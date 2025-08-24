# /bot_portal/models.py
from db import get_db
import psycopg2.extras # Импортируем DictCursor

class EditorModel:
    @staticmethod
    def find_by_id(user_id):
        """
        Находит активного редактора по его user_id.
        """
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT user_id, username FROM editors WHERE user_id = %s AND is_inactive = FALSE",
            (user_id,)
        )
        editor = cur.fetchone()
        cur.close()
        return editor

# --- НАЧАЛО ИЗМЕНЕНИЙ ---
class AppealModel:
    @staticmethod
    def get_all():
        """
        Получает все апелляции из базы данных, отсортированные по дате создания.
        Возвращает список словарей.
        """
        conn = get_db()
        # Используем DictCursor, чтобы получать строки в виде словарей
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            "SELECT case_id, decision_text, status, created_at FROM appeals ORDER BY created_at DESC"
        )
        appeals = cur.fetchall()
        cur.close()
        return appeals
# --- КОНЕЦ ИЗМЕНЕНИЙ ---