# /bot_portal/routes.py
from flask import render_template, request, redirect, url_for, session, current_app, jsonify, abort
from functools import wraps
from . import bot_portal_bp
from .services.auth_service import AuthService
from .services import appeal_service
from .services.gemini_service import GeminiService
from .services.stats_service import StatsService
from .models.rate_limit_model import RateLimitModel
from .models.editor_model import EditorModel
from .models.message_log_model import MessageLogModel

# Декоратор для проверки роли Исполнителя
def executor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'executor':
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

@bot_portal_bp.route('/')
def showcase():
    """
    Отображает главную страницу-витрину портала бота.
    """
    bot_username = current_app.config.get('TELEGRAM_BOT_USERNAME', 'YourBot')
    return render_template('showcase.html', bot_username=bot_username)

@bot_portal_bp.route('/dashboard')
def dashboard():
    """
    Главная страница панели управления. Требует авторизации.
    """
    if not session.get('logged_in'):
        return redirect(url_for('bot_portal.login'))

    stats = StatsService.get_dashboard_stats()
    return render_template('dashboard.html', user=session, stats=stats)

@bot_portal_bp.route('/archive')
def archive():
    """
    Отображает страницу с архивом всех дел с возможностью сортировки.
    """
    if not session.get('logged_in'):
        return redirect(url_for('bot_portal.login'))

    sort_by = request.args.get('sort_by', 'created_at')
    order = request.args.get('order', 'desc')

    appeals_list = appeal_service.get_all_appeals_for_display(sort_by=sort_by, order=order)

    return render_template(
        'archive.html',
        appeals=appeals_list,
        current_sort=sort_by,
        current_order=order
    )

@bot_portal_bp.route('/archive/<int:case_id>')
def appeal_detail(case_id):
    """
    Отображает страницу с детальной информацией по одному делу.
    """
    if not session.get('logged_in'):
        return redirect(url_for('bot_portal.login'))

    appeal_details = appeal_service.get_appeal_details(case_id)

    if not appeal_details:
        return "Дело не найдено", 404

    return render_template('appeal_detail.html', appeal=appeal_details)

@bot_portal_bp.route('/ai-assistant', methods=['GET', 'POST'])
def ai_assistant():
    """
    Обрабатывает страницу ИИ-ассистента.
    """
    if not session.get('logged_in'):
        if request.method == 'POST':
            return jsonify({"error": "Требуется авторизация."}), 401
        return redirect(url_for('bot_portal.login'))

    if request.method == 'POST':
        data = request.get_json()
        question = data.get('question', '')
        user_id = session['user_id']

        if not question:
            return jsonify({"error": "Вопрос не может быть пустым."}), 400

        try:
            RateLimitModel.log_request(user_id)
        except Exception as e:
            current_app.logger.warning(f"Не удалось записать ai_requests_log: {e}")

        response = GeminiService.ask_question(user_id, question)
        return jsonify(response)

    return render_template('ai_assistant.html')

@bot_portal_bp.route('/login')
def login():
    """
    Отображает страницу входа.
    """
    bot_username = current_app.config.get('TELEGRAM_BOT_USERNAME', 'YourBot')
    commit_hash = current_app.config.get('COMMIT_HASH', 'N/A')
    github_url = "https://github.com/honjireview/HJR-Site"
    return render_template('login.html',
                           bot_username=bot_username,
                           commit_hash=commit_hash,
                           github_url=github_url)

@bot_portal_bp.route('/auth/telegram')
def handle_login():
    """
    Обрабатывает колбэк от виджета Telegram.
    """
    auth_data = request.args.to_dict()
    success, message = AuthService.authenticate_user(auth_data)

    if success:
        return redirect(url_for('bot_portal.dashboard'))
    else:
        return f"Ошибка авторизации: {message}", 403

@bot_portal_bp.route('/logout')
def logout():
    """
    Выход из системы.
    """
    AuthService.logout_user()
    return redirect(url_for('bot_portal.showcase'))

@bot_portal_bp.route('/logs')
def portal_logs_shortcut():
    """
    Короткая ссылка на админ-страницу логов.
    """
    if not session.get('logged_in'):
        return redirect(url_for('bot_portal.login'))
    return redirect(url_for('logs.logs_index'))

@bot_portal_bp.route('/editors')
@executor_required
def editors_list():
    """
    Отображает страницу управления редакторами. Доступно только для 'executor'.
    """
    editors = EditorModel.get_all_editors()
    return render_template('editors.html', editors=editors, user=session)

@bot_portal_bp.route('/editors/update-status', methods=['POST'])
@executor_required
def update_editor_status():
    """
    Обрабатывает AJAX-запрос на изменение статуса редактора.
    """
    data = request.get_json()
    user_id = data.get('user_id')
    is_inactive = data.get('is_inactive')

    if user_id is None or is_inactive is None:
        return jsonify({"success": False, "error": "Missing parameters"}), 400

    if int(user_id) == session.get('user_id'):
        return jsonify({"success": False, "error": "You cannot change your own status."}), 403

    success = EditorModel.update_status(user_id, is_inactive)

    if success:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Database update failed"}), 500

# --- НАЧАЛО ИЗМЕНЕНИЙ: Новый маршрут для просмотра активности редактора ---
@bot_portal_bp.route('/editors/<int:user_id>/activity')
@executor_required
def editor_activity(user_id):
    """
    Отображает страницу с логами активности конкретного редактора.
    """
    page = request.args.get('page', 1, type=int)
    per_page = 25 # Установим фиксированное количество логов на страницу

    editor = EditorModel.find_by_id(user_id)
    if not editor:
        abort(404)

    logs, total = MessageLogModel.get_logs_by_author(user_id, page=page, per_page=per_page)

    pages = (total + per_page - 1) // per_page

    return render_template(
        'editor_activity.html',
        editor=editor,
        logs=logs,
        page=page,
        pages=pages,
        total=total
    )
# --- КОНЕЦ ИЗМЕНЕНИЙ ---