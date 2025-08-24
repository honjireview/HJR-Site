# /bot_portal/routes.py
from flask import render_template, request, redirect, url_for, session
from . import bot_portal_bp
from .services import AuthService

@bot_portal_bp.route('/dashboard')
def dashboard():
    """
    Главная страница портала бота. Требует авторизации.
    """
    if not session.get('logged_in'):
        return redirect(url_for('bot_portal.login'))

    return render_template('dashboard.html', user=session)

@bot_portal_bp.route('/login')
def login():
    """
    Отображает страницу входа.
    """
    return render_template('login.html', bot_username=os.getenv("TELEGRAM_BOT_USERNAME", "ВашБот"))

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
        # В реальной системе здесь может быть страница с ошибкой
        return f"Ошибка авторизации: {message}", 403

@bot_portal_bp.route('/logout')
def logout():
    """
    Выход из системы.
    """
    AuthService.logout_user()
    return redirect(url_for('bot_portal.login'))