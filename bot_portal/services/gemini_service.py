# /bot_portal/services/gemini_service.py
import os
import logging
import google.generativeai as genai
from ..models.rate_limit_model import RateLimitModel

log = logging.getLogger(__name__)

# Конфигурация Gemini API при загрузке модуля
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    log.warning("GEMINI_API_KEY не установлен. GeminiService не будет работать.")

class GeminiService:
    # Системные лимиты
    MAX_QUESTION_LENGTH = 2000
    MAX_REQUESTS = 10
    RATE_LIMIT_HOURS = 3

    @staticmethod
    def _read_file(filepath, default_text=""):
        """Безопасно читает текстовый файл."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            log.error(f"Файл не найден: {filepath}")
            return default_text

    @staticmethod
    def ask_question(user_id, question_text):
        """
        Обрабатывает вопрос пользователя, проверяет лимиты и обращается к Gemini.
        """
        # 1. Проверка длины сообщения
        if len(question_text) > GeminiService.MAX_QUESTION_LENGTH:
            log.warning(f"Пользователь {user_id} превысил лимит длины сообщения.")
            return {"error": f"Ваш вопрос слишком длинный. Максимальная длина: {GeminiService.MAX_QUESTION_LENGTH} символов."}

        # 2. Проверка лимита запросов
        recent_requests = RateLimitModel.count_recent_requests(user_id, hours=GeminiService.RATE_LIMIT_HOURS)
        log.debug(f"Пользователь {user_id} сделал {recent_requests}/{GeminiService.MAX_REQUESTS} запросов за последние {GeminiService.RATE_LIMIT_HOURS} часа.")
        if recent_requests >= GeminiService.MAX_REQUESTS:
            log.warning(f"Пользователь {user_id} превысил лимит запросов.")
            return {"error": f"Вы превысили лимит запросов ({GeminiService.MAX_REQUESTS} за {GeminiService.RATE_LIMIT_HOURS} часа). Пожалуйста, попробуйте позже."}

        # 3. Формирование промпта
        instructions = GeminiService._read_file('gemini_instructions.txt', "Отвечай только на вопросы по правилам.")
        rules_context = GeminiService._read_file('rules.txt', "Правила не найдены.")

        prompt = f"""
{instructions}

--- НАЧАЛО КОНТЕКСТА (ПРАВИЛА ПРОЕКТА) ---
{rules_context}
--- КОНЕЦ КОНТЕКСТА ---

Вопрос пользователя: "{question_text}"
"""
        # 4. Обращение к Gemini API
        if not GEMINI_API_KEY:
            return {"error": "Сервис ИИ-ассистента временно недоступен."}

        try:
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
            response = model.generate_content(prompt)

            # 5. Логирование успешного запроса
            RateLimitModel.log_request(user_id)
            log.info(f"Успешный запрос к Gemini от пользователя {user_id}.")

            return {"answer": response.text}
        except Exception as e:
            log.error(f"Ошибка при обращении к Gemini API: {e}")
            return {"error": "Произошла внутренняя ошибка при обработке вашего запроса."}