# /bot_portal/services.py
import os
import hmac
import hashlib
import time
import logging
from flask import session
from .models import EditorModel

# Настройка логгера для этого модуля
log = logging.getLogger(__name__)

class AuthService:
    @staticmethod
    def _is_telegram_data_valid(auth_data):
        """
        Криптографическая проверка подлинности данных от Telegram.
        """
        BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
        if not BOT_TOKEN:
            log.error("[AUTH_VALIDATION] Критическая ошибка: TELEGRAM_TOKEN не установлен.")
            return False

        received_hash = auth_data.pop('hash')
        log.debug(f"[AUTH_VALIDATION] Полученный хэш: {received_hash}")

        data_check_string = "\n".join(sorted([f"{k}={v}" for k, v in auth_data.items()]))
        log.debug(f"[AUTH_VALIDATION] Строка для проверки: \n---\n{data_check_string}\n---")

        secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        log.debug(f"[AUTH_VALIDATION] Рассчитанный хэш: {calculated_hash}")

        is_valid = calculated_hash == received_hash
        if not is_valid:
            log.warning("[AUTH_VALIDATION] ПРОВАЛ: Хэши не совпадают. Возможна попытка подделки.")
        else:
            log.info("[AUTH_VALIDATION] УСПЕХ: Криптографическая подпись данных верна.")

        return is_valid

    @staticmethod
    def _create_user_session(user_data):
        """
        Создает сессию для пользователя.
        """
        session.clear()
        session['user_id'] = int(user_data['id'])
        session['username'] = user_data.get('username', 'N/A')
        session['first_name'] = user_data.get('first_name', 'N/A')
        session['logged_in'] = True
        log.info(f"[AUTH_SESSION] УСПЕХ: Сессия создана для пользователя user_id={session['user_id']} (@{session['username']}).")

    # --- НАЧАЛО ИСПРАВЛЕНИЙ: ВОССТАНОВЛЕНИЕ НЕДОСТАЮЩЕГО МЕТОДА ---
    @staticmethod
    def authenticate_user(auth_data):
        """
        Оркестрирует процесс аутентификации. Возвращает (успех, сообщение/объект).
        """
        log.info(f"--- [AUTH_START] Начало процесса аутентификации для пользователя id={auth_data.get('id')} ---")

        # 1. Проверка срока действия
        auth_date = int(auth_data.get('auth_date', 0))
        current_time = time.time()
        log.debug(f"[AUTH_TIME_CHECK] Время сервера: {current_time}, Время данных: {auth_date}, Разница: {current_time - auth_date} сек.")
        if current_time - auth_date > 60:
            log.warning(f"[AUTH_TIME_CHECK] ПРОВАЛ: Данные аутентификации устарели (прошло {current_time - auth_date} сек).")
            return False, "Данные аутентификации устарели. Пожалуйста, попробуйте снова."
        log.info("[AUTH_TIME_CHECK] УСПЕХ: Срок действия данных в норме.")

        # 2. Проверка подписи
        if not AuthService._is_telegram_data_valid(auth_data.copy()):
            return False, "Неверная подпись данных. Попытка подделки запроса."

        # 3. Проверка прав доступа
        user_id = int(auth_data['id'])
        log.debug(f"[AUTH_PERMISSIONS] Проверка прав для user_id={user_id} в базе данных...")
        editor = EditorModel.find_by_id(user_id)
        if not editor:
            log.warning(f"[AUTH_PERMISSIONS] ПРОВАЛ: Пользователь user_id={user_id} не найден в таблице активных редакторов.")
            return False, "Доступ запрещен. Вы не являетесь активным редактором."
        log.info(f"[AUTH_PERMISSIONS] УСПЕХ: Пользователь user_id={user_id} является активным редактором.")

        # 4. Создание сессии
        AuthService._create_user_session(auth_data)
        log.info(f"--- [AUTH_END] Аутентификация для user_id={user_id} завершена успешно. ---")
        return True, "Аутентификация прошла успешно."
    # --- КОНЕЦ ИСПРАВЛЕНИЙ ---

    @staticmethod
    def logout_user():
        """
        Завершает сессию пользователя.
        """
        user_id = session.get('user_id', 'N/A')
        session.clear()
        log.info(f"[AUTH_SESSION] Сессия для пользователя user_id={user_id} была завершена.")