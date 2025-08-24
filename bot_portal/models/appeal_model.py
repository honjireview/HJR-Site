# /bot_portal/models/appeal_model.py
from db import get_db
import psycopg2.extras

class AppealModel:
    @staticmethod
    def get_all(sort_by='created_at', order='desc'):
        """
        Получает все апелляции из БД с возможностью сортировки.
        """
        allowed_sort_columns = ['case_id', 'status', 'created_at']
        allowed_orders = ['asc', 'desc']

        sort_column = sort_by if sort_by in allowed_sort_columns else 'created_at'
        sort_order = order if order in allowed_orders else 'desc'

        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = f"SELECT case_id, decision_text, status, created_at FROM appeals ORDER BY {sort_column} {sort_order}"

        cur.execute(query)
        appeals = cur.fetchall()
        cur.close()
        return appeals

    @staticmethod
    def find_by_id(case_id):
        """
        Находит одну апелляцию по ее case_id и возвращает все данные.
        """
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM appeals WHERE case_id = %s", (case_id,))
        appeal = cur.fetchone()
        cur.close()
        return appeal