# /bot_portal/models/rate_limit_model.py
from db import get_db
from datetime import datetime, timedelta

class RateLimitModel:
    @staticmethod
    def log_request(user_id):
        """
        Записывает факт одного запроса от пользователя в лог.
        """
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO ai_requests_log (user_id, timestamp) VALUES (%s, %s)",
            (user_id, datetime.utcnow())
        )
        conn.commit()
        cur.close()

    @staticmethod
    def count_recent_requests(user_id, hours=3):
        """
        Считает количество запросов от пользователя за последние N часов.
        """
        conn = get_db()
        cur = conn.cursor()
        time_threshold = datetime.utcnow() - timedelta(hours=hours)
        cur.execute(
            "SELECT COUNT(*) FROM ai_requests_log WHERE user_id = %s AND timestamp >= %s",
            (user_id, time_threshold)
        )
        count = cur.fetchone()[0]
        cur.close()
        return count

    # --- НАЧАЛО ИЗМЕНЕНИЙ ---
    @staticmethod
    def get_total_count():
        """
        Возвращает общее количество запросов к ИИ.
        """
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM ai_requests_log")
        count = cur.fetchone()[0]
        cur.close()
        return count
    # --- КОНЕЦ ИЗМЕНЕНИЙ ---