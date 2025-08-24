# /bot_portal/models.py
from db import get_db

class EditorModel:
    @staticmethod
    def find_by_id(user_id):
        """
        Находит активного редактора по его user_id.
        Возвращает кортеж (user_id, username) или None.
        """
        conn = get_db()
        # Используем cursor_factory для получения словарей вместо кортежей
        cur = conn.cursor()
        cur.execute(
            "SELECT user_id, username FROM editors WHERE user_id = %s AND is_inactive = FALSE",
            (user_id,)
        )
        editor = cur.fetchone()
        cur.close()
        return editor