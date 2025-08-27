# /bot_portal/services/appeal_service.py
from db import get_db
import psycopg2.extras

def _map_status(status_string):
    """
    Преобразует текстовый статус в объект с текстом и цветом для фронтенда.
    """
    status_map = {
        'closed': {'text': 'Закрыто', 'color': 'green'},
        'closed_after_review': {'text': 'Закрыто после пересмотра', 'color': 'yellow'},
        'reviewing': {'text': 'На рассмотрении', 'color': 'blue'},
        'pending_council': {'text': 'Ожидает Совет', 'color': 'purple'},
        'pending_ai_verdict': {'text': 'Ожидает вердикт ИИ', 'color': 'indigo'}
    }
    if not status_string:
        return {'text': 'Статус не задан', 'color': 'slate'}
    return status_map.get(status_string, {'text': status_string, 'color': 'slate'})

def _process_appeal_for_display(appeal_row):
    """
    Централизованная функция для обработки одной записи апелляции для отображения.
    """
    if not appeal_row:
        return None

    processed_appeal = dict(appeal_row)
    processed_appeal['status_obj'] = _map_status(processed_appeal.get('status'))

    # Добавляем заглушки для пустых, но важных полей
    if not processed_appeal.get('decision_text'):
        processed_appeal['decision_text'] = '[Предмет спора не указан]'
    if not processed_appeal.get('applicant_answers'):
        processed_appeal['applicant_answers'] = {
            'main_arguments': '[Аргументы не предоставлены]',
            'violated_rule': '[Пункт не указан]',
            'desired_outcome': '[Результат не указан]',
            'context': '[Контекст не предоставлен]'
        }

    return processed_appeal

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
    appeals_raw = cur.fetchall()
    cur.close()

    return [_process_appeal_for_display(appeal) for appeal in appeals_raw]

# Получение детальной информации по одному делу
def get_appeal_details(case_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM appeals WHERE case_id = %s", (case_id,))
    appeal_raw = cur.fetchone()
    cur.close()

    return _process_appeal_for_display(appeal_raw)

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