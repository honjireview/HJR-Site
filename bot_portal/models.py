# /bot_portal/models.py
from db import get_db
import psycopg2.extras

class EditorModel:
    @staticmethod
    def find_by_id(user_id):
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT user_id, username FROM editors WHERE user_id = %s AND is_inactive = FALSE",
            (user_id,)
        )
        editor = cur.fetchone()
        cur.close()
        return editor

class AppealModel:
    # --- НАЧАЛО ИЗМЕНЕНИЙ ---
    @staticmethod
    def get_all(sort_by='created_at', order='desc'):
        """
        Получает все апелляции из БД с возможностью сортировки.
        """
        # Белый список для предотвращения SQL-инъекций
        allowed_sort_columns = ['case_id', 'status', 'created_at']
        allowed_orders = ['asc', 'desc']

        # Проверка параметров на соответствие белому списку
        sort_column = sort_by if sort_by in allowed_sort_columns else 'created_at'
        sort_order = order if order in allowed_orders else 'desc'

        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Динамическое, но безопасное формирование запроса
        query = f"SELECT case_id, decision_text, status, created_at FROM appeals ORDER BY {sort_column} {sort_order}"

        cur.execute(query)
        appeals = cur.fetchall()
        cur.close()
        return appeals
    # --- КОНЕЦ ИЗМЕНЕНИЙ ---

    @staticmethod
    def find_by_id(case_id):
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM appeals WHERE case_id = %s", (case_id,))
        appeal = cur.fetchone()
        cur.close()
        return appeal