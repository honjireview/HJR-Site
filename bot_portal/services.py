# /bot_portal/services.py
import os
import hmac
import hashlib
import time
from flask import session
from .models import EditorModel

class AuthService:
    @staticmethod
    def _is_telegram_data_valid(auth_data):
        """
        Криптографическая проверка подлинности данных от Telegram.
        """
        BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
        if not BOT_TOKEN:
            # В реальной системе здесь должно быть логирование ошибки
            return False

        received_hash = auth_data.pop('hash')
        data_check_string = "\n".join(sorted([f"{k}={v}" for k, v in auth_data.items()]))

        secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

        return calculated_hash == received_hash

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

    @staticmethod
    def authenticate_user(auth_data):
        """
        Оркестрирует процесс аутентификации. Возвращает (успех, сообщение/объект).
        """
        # 1. Проверка срока действия
        if time.time() - int(auth_data.get('auth_date', 0)) > 300: # 5 минут
            return False, "Данные аутентификации устарели."

        # 2. Проверка подписи
        if not AuthService._is_telegram_data_valid(auth_data.copy()):
            return False, "Неверная подпись данных. Попытка подделки запроса."

        # 3. Проверка прав доступа
        user_id = int(auth_data['id'])
        editor = EditorModel.find_by_id(user_id)
        if not editor:
            return False, "Доступ запрещен. Вы не являетесь активным редактором."

        # 4. Создание сессии
        AuthService._create_user_session(auth_data)
        return True, "Аутентификация прошла успешно."

    @staticmethod
    def logout_user():
        """
        Завершает сессию пользователя.
        """
        session.clear()