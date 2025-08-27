# /bot_portal/models/appeal_model.py
from db import get_db
import psycopg2.extras

# Получение списка апелляций с сортировкой для отображения в архиве
def get_all_appeals_for_display(sort_by='created_at', order='desc'):
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

# Получение детальной информации по одному делу
def get_appeal_details(case_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM appeals WHERE case_id = %s", (case_id,))
    appeal = cur.fetchone()
    cur.close()
    return appeal

# Статистика по апелляциям для дашборда
def get_appeals_stats():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            COUNT(*) AS total,
            COUNT(CASE WHEN status = 'closed' THEN 1 END) AS closed,
            COUNT(CASE WHEN status = 'closed_after_review' THEN 1 END) AS closed_after_review,
            COUNT(CASE WHEN status = 'reviewing' THEN 1 END) AS reviewing
        FROM appeals;
    """)
    total, closed, closed_after_review, reviewing = cur.fetchone()
    cur.close()
    return {
        "total": total,
        "statuses": {
            "closed": closed,
            "closed_after_review": closed_after_review,
            "reviewing": reviewing
        }
    }