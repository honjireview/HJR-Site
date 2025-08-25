# /bot_portal/models/message_log_model.py
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
from db import get_db
import psycopg2.extras

class MessageLogModel:
    allowed_sort_columns = [
        'logged_at', 'created_at', 'message_id', 'chat_id', 'author_user_id', 'content_type'
    ]
    allowed_orders = ['asc', 'desc']

    @staticmethod
    def list_logs(
        page: int = 1,
        per_page: int = 50,
        sort_by: str = 'logged_at',
        order: str = 'desc',
        filters: Optional[Dict[str, Any]] = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Возвращает список логов и общее количество записей для пагинации.
        filters может содержать ключи: chat_id, author_user_id, content_type,
        date_from (datetime), date_to (datetime), has_file (bool), q (строка поиска по text).
        """
        filters = filters or {}
        sort_col = sort_by if sort_by in MessageLogModel.allowed_sort_columns else 'logged_at'
        sort_order = order if order in MessageLogModel.allowed_orders else 'desc'

        where_clauses = []
        params = []

        if filters.get('chat_id') is not None:
            where_clauses.append("chat_id = %s")
            params.append(filters['chat_id'])

        if filters.get('author_user_id') is not None:
            where_clauses.append("author_user_id = %s")
            params.append(filters['author_user_id'])

        if filters.get('content_type'):
            where_clauses.append("content_type = %s")
            params.append(filters['content_type'])

        if filters.get('has_file') is True:
            where_clauses.append("file_id IS NOT NULL AND file_id <> ''")
        elif filters.get('has_file') is False:
            where_clauses.append("(file_id IS NULL OR file_id = '')")

        if filters.get('date_from'):
            where_clauses.append("logged_at >= %s")
            params.append(filters['date_from'])

        if filters.get('date_to'):
            where_clauses.append("logged_at <= %s")
            params.append(filters['date_to'])

        if filters.get('q'):
            where_clauses.append("(text ILIKE %s OR chat_title ILIKE %s OR topic_name ILIKE %s)")
            q = f"%{filters['q']}%"
            params.extend([q, q, q])

        where_sql = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""

        offset = (page - 1) * per_page

        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Общее количество
        count_sql = f"SELECT COUNT(*) FROM message_log{where_sql}"
        cur.execute(count_sql, params)
        total = cur.fetchone()[0]

        # Данные страницы
        data_sql = f"""
            SELECT
              internal_id, message_id, chat_id, chat_type, chat_title,
              topic_id, topic_name,
              author_user_id, author_username, author_first_name, author_is_bot,
              text, content_type, file_id,
              reply_to_message_id, forward_from_chat_id, forward_from_message_id,
              created_at, last_edited_at, edit_history, logged_at
            FROM message_log
            {where_sql}
            ORDER BY {sort_col} {sort_order}
            LIMIT %s OFFSET %s
        """
        cur.execute(data_sql, [*params, per_page, offset])
        rows = cur.fetchall()
        cur.close()

        return [dict(r) for r in rows], total

    @staticmethod
    def get_by_internal_id(internal_id: int) -> Optional[Dict[str, Any]]:
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            """
            SELECT
              internal_id, message_id, chat_id, chat_type, chat_title,
              topic_id, topic_name,
              author_user_id, author_username, author_first_name, author_is_bot,
              text, content_type, file_id,
              reply_to_message_id, forward_from_chat_id, forward_from_message_id,
              created_at, last_edited_at, edit_history, logged_at
            FROM message_log
            WHERE internal_id = %s
            """,
            (internal_id,)
        )
        row = cur.fetchone()
        cur.close()
        return dict(row) if row else None