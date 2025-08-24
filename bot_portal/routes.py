# /bot_portal/routes.py
from flask import render_template, request, redirect, url_for, session, current_app, jsonify
from . import bot_portal_bp
# --- НАЧАЛО ИЗМЕНЕНИЙ: Исправлен импорт сервисов на явные модульные импорты ---
from .services.auth_service import AuthService
from .services.appeal_service import AppealService
from .services.gemini_service import GeminiService
# --- КОНЕЦ ИЗМЕНЕНИЙ ---

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

    return render_template('dashboard.html', user=session)

@bot_portal_bp.route('/archive')
def archive():
    """
    Отображает страницу с архивом всех дел с возможностью сортировки.
    """
    if not session.get('logged_in'):
        return redirect(url_for('bot_portal.login'))

    sort_by = request.args.get('sort_by', 'created_at')
    order = request.args.get('order', 'desc')

    appeals_list = AppealService.get_all_appeals_for_display(sort_by=sort_by, order=order)

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

    appeal_details = AppealService.get_appeal_details(case_id)

    if not appeal_details:
        return "Дело не найдено", 404

    return render_template('appeal_detail.html', appeal=appeal_details)

@bot_portal_bp.route('/ai-assistant', methods=['GET', 'POST'])
def ai_assistant():
    """
    Обрабатывает страницу ИИ-ассистента.
    GET - отображает страницу.
    POST - обрабатывает AJAX-запрос с вопросом.
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

        response = GeminiService.ask_question(user_id, question)
        return jsonify(response)

    return render_template('ai_assistant.html')

@bot_portal_bp.route('/login')
def login():
    """
    Отображает страницу входа.
    """
    bot_username = current_app.config.get('TELEGRAM_BOT_USERNAME', 'YourBot')
    return render_template('login.html', bot_username=bot_username)

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