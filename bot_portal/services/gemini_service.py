# /bot_portal/services/gemini_service.py
import os
import logging
import google.generativeai as genai
from ..models.rate_limit_model import RateLimitModel
from ..models.ai_chat_history_model import AiChatHistoryModel

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

        # 1. Проверки лимитов
        if len(question_text) > GeminiService.MAX_QUESTION_LENGTH:
            log.warning(f"[GEMINI_ASK] ПРОВАЛ: Длина сообщения превышена ({len(question_text)} > {GeminiService.MAX_QUESTION_LENGTH}).")
            return {"error": f"Ваш вопрос слишком длинный. Максимальная длина: {GeminiService.MAX_QUESTION_LENGTH} символов."}

        recent_requests = RateLimitModel.count_recent_requests(user_id, hours=GeminiService.RATE_LIMIT_HOURS)
        if recent_requests >= GeminiService.MAX_REQUESTS:
            log.warning(f"[GEMINI_ASK] ПРОВАЛ: Пользователь {user_id} превысил лимит запросов.")
            return {"error": f"Вы превысили лимит запросов ({GeminiService.MAX_REQUESTS} за {GeminiService.RATE_LIMIT_HOURS} часа). Пожалуйста, попробуйте позже."}
        log.info("[GEMINI_ASK] УСПЕХ: Проверки лимитов пройдены.")

        # 2. Логирование вопроса пользователя
        try:
            AiChatHistoryModel.log_message(user_id, 'user', question_text)
            log.info(f"[GEMINI_ASK] Вопрос от user_id={user_id} залогирован.")
        except Exception as e:
            log.error(f"[GEMINI_ASK] ОШИБКА: Не удалось залогировать вопрос пользователя: {e}")

        # 3. Формирование промпта и обращение к API
        if not GEMINI_API_KEY:
            log.error("[GEMINI_ASK] ПРОВАЛ: GEMINI_API_KEY не доступен.")
            return {"error": "Сервис ИИ-ассистента временно недоступен."}

        ai_answer = ""
        error_message = None

        try:
            instructions = GeminiService._read_file('gemini_instructions.txt', "Отвечай только на вопросы по правилам.")
            rules_context = GeminiService._read_file('rules.txt', "Правила не найдены.")
            prompt = f"{instructions}\n\n--- КОНТЕКСТ ---\n{rules_context}\n--- КОНЕЦ КОНТЕКСТА ---\n\nВопрос: \"{question_text}\""

            log.info("[GEMINI_ASK] Отправка запроса в Gemini API...")
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
            response = model.generate_content(prompt)
            ai_answer = response.text or "[ИИ не дал ответа]"
            log.info("[GEMINI_ASK] УСПЕХ: Ответ от Gemini API получен.")

            # Логируем успешный запрос для rate limit'а
            RateLimitModel.log_request(user_id)
            log.info(f"[GEMINI_ASK] Запрос для user_id={user_id} засчитан в лимитах.")

        except Exception as e:
            log.error(f"[GEMINI_ASK] КРИТИЧЕСКАЯ ОШИБКА при обращении к Gemini API: {e}")
            error_message = "Произошла внутренняя ошибка при обработке вашего запроса."
            ai_answer = f"[ОШИБКА СЕРВЕРА: {e}]" # Запишем ошибку в лог чата

        finally:
            # 4. Логирование ответа ИИ (происходит всегда)
            try:
                AiChatHistoryModel.log_message(user_id, 'ai', ai_answer)
                log.info(f"[GEMINI_ASK] Ответ ИИ для user_id={user_id} залогирован.")
            except Exception as e:
                log.error(f"[GEMINI_ASK] ОШИБКА: Не удалось залогировать ответ ИИ: {e}")

            log.info(f"--- [GEMINI_ASK_END] Обработка запроса от user_id={user_id} завершена ---")

        if error_message:
            return {"error": error_message}
        else:
            return {"answer": ai_answer}