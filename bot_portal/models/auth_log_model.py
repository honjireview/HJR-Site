# /bot_portal/models/auth_log_model.py
from db import get_db
from datetime import datetime

class AuthLogModel:
    @staticmethod
    def log_login(user_id, username, first_name):
        """
        Записывает факт успешного входа пользователя.
        """
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO auth_logs (user_id, username, first_name, timestamp) VALUES (%s, %s, %s, %s)",
            (user_id, username, first_name, datetime.utcnow())
        )
        conn.commit()
        cur.close()