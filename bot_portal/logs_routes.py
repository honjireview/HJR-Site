# /bot_portal/logs_routes.py
from flask import Blueprint, render_template, request
from datetime import datetime
from .models.message_log_model import MessageLogModel

logs_bp = Blueprint(
    'logs',
    __name__,
    template_folder='../templates/bot_portal'
)


@logs_bp.route('/logs')
def logs_index():
    # Параметры запроса
    page = max(int(request.args.get('page', 1)), 1)
    per_page = min(max(int(request.args.get('per_page', 50)), 1), 200)

    sort_by = request.args.get('sort_by', 'logged_at')
    order = request.args.get('order', 'desc')

    # --- НАЧАЛО ИЗМЕНЕНИЙ: Добавляем фильтр по chat_type ---
    active_chat_type = request.args.get('chat_type')
    # --- КОНЕЦ ИЗМЕНЕНИЙ ---

    filters = {}
    if request.args.get('chat_id'):
        try:
            filters['chat_id'] = int(request.args['chat_id'])
        except ValueError:
            pass

    # --- НАЧАЛО ИЗМЕНЕНИЙ: Интегрируем фильтр chat_type в основной запрос ---
    if active_chat_type in ('supergroup', 'channel'):
        filters['chat_type'] = active_chat_type
    # --- КОНЕЦ ИЗМЕНЕНИЙ ---

    if request.args.get('author_user_id'):
        try:
            filters['author_user_id'] = int(request.args['author_user_id'])
        except ValueError:
            pass

    if request.args.get('content_type'):
        filters['content_type'] = request.args['content_type']

    if request.args.get('has_file') in ('true', 'false'):
        filters['has_file'] = request.args.get('has_file') == 'true'

    # Дата в формате ISO (YYYY-MM-DD)
    if request.args.get('date_from'):
        try:
            filters['date_from'] = datetime.fromisoformat(request.args['date_from'])
        except ValueError:
            pass

    if request.args.get('date_to'):
        try:
            # до конца дня включительно
            filters['date_to'] = datetime.fromisoformat(request.args['date_to'])
        except ValueError:
            pass

    if request.args.get('q'):
        filters['q'] = request.args['q']

    data, total = MessageLogModel.list_logs(
        page=page,
        per_page=per_page,
        sort_by=sort_by,
        order=order,
        filters=filters
    )

    pages = (total + per_page - 1) // per_page

    def get_paginated_url(p, ct=active_chat_type):
        args = request.args.to_dict(flat=True)
        args['page'] = p
        if ct:
            args['chat_type'] = ct
        else:
            args.pop('chat_type', None)
        return f"{request.base_url}?{'&'.join(f'{k}={v}' for k, v in args.items())}"

    prev_url = get_paginated_url(page - 1) if page > 1 else None
    next_url = get_paginated_url(page + 1) if page < pages else None

    return render_template(
        'bot_portal/logs.html',
        items=data,
        page=page,
        per_page=per_page,
        pages=pages,
        total=total,
        sort_by=sort_by,
        order=order,
        filters=filters,
        prev_url=prev_url,
        next_url=next_url,
        active_chat_type=active_chat_type # Передаем активный тип чата в шаблон
    )


@logs_bp.route('/logs/<int:internal_id>')
def logs_view(internal_id: int):
    item = MessageLogModel.get_by_internal_id(internal_id)
    return render_template('bot_portal/logs_view.html', item=item)