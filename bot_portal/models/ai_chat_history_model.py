from db import get_db
from datetime import datetime

class AiChatHistoryModel:
    @staticmethod
    def log_message(user_id, sender, message_text):
        """
        Записывает сообщение в историю чата с ИИ.
        """
        conn = get_db()
        cur = conn.cursor()
        # Примечание: SQL-запрос адаптирован для совместимости с PostgreSQL и SQLite.
        # В PostgreSQL NOW() вернет TIMESTAMPTZ, в SQLite (datetime('now')) вернет текстовую дату.
        sql = """
              INSERT INTO ai_chat_history (user_id, sender, message_text, timestamp)
              VALUES (%s, %s, %s, NOW()) \
              """
        # Адаптация для SQLite
        if 'sqlite' in str(type(conn)).lower():
            sql = sql.replace('%s', '?').replace('NOW()', "datetime('now')")

        cur.execute(sql, (user_id, sender, message_text))

        if 'psycopg2' in str(type(conn.cursor())).__module__.lower():
            conn.commit() # 커밋은 psycopg2에만 필요합니다

        cur.close()