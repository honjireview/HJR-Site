# /bot_portal/models/editor_model.py
from db import get_db

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