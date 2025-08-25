# /bot_portal/services/gemini_service.py
import os
import logging
import google.generativeai as genai
from ..models.rate_limit_model import RateLimitModel
from ..models.ai_chat_history_model import AiChatHistoryModel # <-- Импортирована модель для логирования

log = logging.getLogger(__name__)

# --- Логирование при старте модуля ---
log.info("[GEMINI_SERVICE] Модуль загружается...")
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        log.info("[GEMINI_SERVICE] УСПЕХ: Конфигурация Gemini API прошла успешно.")
    except Exception as e:
        log.critical(f"[GEMINI_SERVICE] КРИТИЧЕСКАЯ ОШИБКА при конфигурации Gemini API: {e}")
else:
    log.warning("[GEMINI_SERVICE] ВНИМАНИЕ: GEMINI_API_KEY не установлен. Сервис не будет работать.")

class GeminiService:
    # Системные лимиты
    MAX_QUESTION_LENGTH = 2000
    MAX_REQUESTS = 10
    RATE_LIMIT_HOURS = 3

    @staticmethod
    def _read_file(filepath, default_text=""):
        log.debug(f"[GEMINI_SERVICE] Попытка чтения файла: {filepath}")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                log.debug(f"[GEMINI_SERVICE] УСПЕХ: Файл {filepath} успешно прочитан ({len(content)} символов).")
                return content
        except FileNotFoundError:
            log.error(f"[GEMINI_SERVICE] ОШИБКА: Файл не найден: {filepath}")
            return default_text

    @staticmethod
    def ask_question(user_id, question_text):
        """
        Обрабатывает вопрос пользователя, проверяет лимиты и обращается к Gemini.
        """
        log.info(f"--- [GEMINI_ASK_START] Начало обработки запроса от user_id={user_id} ---")

        # 1. Проверка длины сообщения
        if len(question_text) > GeminiService.MAX_QUESTION_LENGTH:
            log.warning(f"[GEMINI_ASK] ПРОВАЛ: Пользователь {user_id} превысил лимит длины сообщения ({len(question_text)} > {GeminiService.MAX_QUESTION_LENGTH}).")
            return {"error": f"Ваш вопрос слишком длинный. Максимальная длина: {GeminiService.MAX_QUESTION_LENGTH} символов."}
        log.info("[GEMINI_ASK] УСПЕХ: Проверка длины сообщения пройдена.")

        # 2. Проверка лимита запросов
        recent_requests = RateLimitModel.count_recent_requests(user_id, hours=GeminiService.RATE_LIMIT_HOURS)
        log.debug(f"[GEMINI_ASK] Проверка лимитов: {recent_requests}/{GeminiService.MAX_REQUESTS} запросов за последние {GeminiService.RATE_LIMIT_HOURS} часа.")
        if recent_requests >= GeminiService.MAX_REQUESTS:
            log.warning(f"[GEMINI_ASK] ПРОВАЛ: Пользователь {user_id} превысил лимит запросов.")
            return {"error": f"Вы превысили лимит запросов ({GeminiService.MAX_REQUESTS} за {GeminiService.RATE_LIMIT_HOURS} часа). Пожалуйста, попробуйте позже."}
        log.info("[GEMINI_ASK] УСПЕХ: Проверка лимитов пройдена.")

        # --- НАЧАЛО ИЗМЕНЕНИЙ: Логирование вопроса пользователя ---
        try:
            AiChatHistoryModel.log_message(user_id, 'user', question_text)
            log.info(f"[GEMINI_ASK] Вопрос от user_id={user_id} залогирован в историю чата.")
        except Exception as e:
            log.error(f"[GEMINI_ASK] ОШИБКА: Не удалось залогировать вопрос пользователя: {e}")
        # --- КОНЕЦ ИЗМЕНЕНИЙ ---

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
        log.debug(f"[GEMINI_ASK] Сформирован промпт. Общая длина: {len(prompt)} символов.")

        # 4. Обращение к Gemini API
        if not GEMINI_API_KEY:
            log.error("[GEMINI_ASK] ПРОВАЛ: GEMINI_API_KEY не доступен.")
            return {"error": "Сервис ИИ-ассистента временно недоступен."}

        try:
            log.info("[GEMINI_ASK] Отправка запроса в Gemini API...")
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
            response = model.generate_content(prompt)
            ai_answer = response.text # Сохраняем ответ в переменную
            log.info("[GEMINI_ASK] УСПЕХ: Ответ от Gemini API получен.")
            log.debug(f"[GEMINI_ASK] Текст ответа (первые 100 символов): {ai_answer[:100]}...")

            # 5. Логирование успешного запроса
            RateLimitModel.log_request(user_id)
            log.info(f"[GEMINI_ASK] Запрос для user_id={user_id} успешно залогирован в БД.")

            # --- НАЧАЛО ИЗМЕНЕНИЙ: Логирование ответа ИИ ---
            try:
                AiChatHistoryModel.log_message(user_id, 'ai', ai_answer)
                log.info(f"[GEMINI_ASK] Ответ ИИ для user_id={user_id} залогирован в историю чата.")
            except Exception as e:
                log.error(f"[GEMINI_ASK] ОШИБКА: Не удалось залогировать ответ ИИ: {e}")
            # --- КОНЕЦ ИЗМЕНЕНИЙ ---

            return {"answer": ai_answer}
        except Exception as e:
            log.error(f"[GEMINI_ASK] КРИТИЧЕСКАЯ ОШИБКА при обращении к Gemini API: {e}")
            return {"error": "Произошла внутренняя ошибка при обработке вашего запроса."}
        finally:
            log.info(f"--- [GEMINI_ASK_END] Обработка запроса от user_id={user_id} завершена ---")