# /bot_portal/models/editor_model.py
from db import get_db
import psycopg2.extras

class EditorModel:
    @staticmethod
    def find_by_id(user_id):
        """
        Находит редактора по его user_id и возвращает все данные.
        """
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            "SELECT user_id, username, first_name, role, is_inactive FROM editors WHERE user_id = %s",
            (user_id,)
        )
        editor = cur.fetchone()
        cur.close()
        return editor

    @staticmethod
    def get_all_editors():
        """
        Возвращает список всех редакторов из базы данных.
        """
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT user_id, username, first_name, role, is_inactive FROM editors ORDER BY first_name ASC")
        editors = cur.fetchall()
        cur.close()
        return editors

    @staticmethod
    def update_status(user_id, is_inactive: bool):
        """
        Обновляет статус is_inactive для указанного редактора.
        """
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "UPDATE editors SET is_inactive = %s WHERE user_id = %s",
            (is_inactive, user_id)
        )
        conn.commit()
        updated_rows = cur.rowcount
        cur.close()
        return updated_rows > 0