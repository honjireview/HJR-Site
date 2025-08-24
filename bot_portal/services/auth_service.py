# /bot_portal/services/auth_service.py
import os
import hmac
import hashlib
import time
import logging
from flask import session
from ..models import EditorModel

log = logging.getLogger(__name__)

class AuthService:
    @staticmethod
    def _is_telegram_data_valid(auth_data):
        BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
        if not BOT_TOKEN:
            log.error("[AUTH_VALIDATION] Критическая ошибка: TELEGRAM_TOKEN не установлен.")
            return False
        received_hash = auth_data.pop('hash')
        data_check_string = "\n".join(sorted([f"{k}={v}" for k, v in auth_data.items()]))
        secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        is_valid = calculated_hash == received_hash
        if not is_valid:
            log.warning("[AUTH_VALIDATION] ПРОВАЛ: Хэши не совпадают.")
        else:
            log.info("[AUTH_VALIDATION] УСПЕХ: Криптографическая подпись данных верна.")
        return is_valid

    @staticmethod
    def _create_user_session(user_data):
        session.clear()
        session['user_id'] = int(user_data['id'])
        session['username'] = user_data.get('username', 'N/A')
        session['first_name'] = user_data.get('first_name', 'N/A')
        session['logged_in'] = True
        log.info(f"[AUTH_SESSION] УСПЕХ: Сессия создана для user_id={session['user_id']} (@{session['username']}).")

    @staticmethod
    def authenticate_user(auth_data):
        log.info(f"--- [AUTH_START] Начало аутентификации для id={auth_data.get('id')} ---")
        auth_date = int(auth_data.get('auth_date', 0))
        current_time = time.time()
        if current_time - auth_date > 60:
            log.warning(f"[AUTH_TIME_CHECK] ПРОВАЛ: Данные устарели (прошло {current_time - auth_date} сек).")
            return False, "Данные аутентификации устарели."
        log.info("[AUTH_TIME_CHECK] УСПЕХ: Срок действия данных в норме.")

        if not AuthService._is_telegram_data_valid(auth_data.copy()):
            return False, "Неверная подпись данных."

        user_id = int(auth_data['id'])
        log.debug(f"[AUTH_PERMISSIONS] Проверка прав для user_id={user_id}...")
        editor = EditorModel.find_by_id(user_id)
        if not editor:
            log.warning(f"[AUTH_PERMISSIONS] ПРОВАЛ: Пользователь user_id={user_id} не является активным редактором.")
            return False, "Доступ запрещен."
        log.info(f"[AUTH_PERMISSIONS] УСПЕХ: Пользователь user_id={user_id} является активным редактором.")

        AuthService._create_user_session(auth_data)
        log.info(f"--- [AUTH_END] Аутентификация для user_id={user_id} завершена успешно. ---")
        return True, "Аутентификация прошла успешно."

    @staticmethod
    def logout_user():
        user_id = session.get('user_id', 'N/A')
        session.clear()
        log.info(f"[AUTH_SESSION] Сессия для user_id={user_id} была завершена.")