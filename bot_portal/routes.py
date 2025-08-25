from flask import render_template, request, redirect, url_for, session, current_app, jsonify
# --- НАЧАЛО ИЗМЕНЕНИЙ: Импортируем блюпринт из __init__.py ---
from . import bot_portal_bp
# --- КОНЕЦ ИЗМЕНЕНИЙ ---
from .services.auth_service import AuthService
# ЗАМЕНА: импортируем модуль вместо несуществующего класса AppealService
from .services import appeal_service
from .services.gemini_service import GeminiService
from .services.stats_service import StatsService
from .models.rate_limit_model import RateLimitModel


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

# ... (остальной код файла остается без изменений) ...

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