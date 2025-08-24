# /bot_portal/routes.py
from flask import render_template, request, redirect, url_for, session, current_app
import os
from . import bot_portal_bp
from .services import AuthService

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

# --- НАЧАЛО ИЗМЕНЕНИЙ ---
@bot_portal_bp.route('/archive')
def archive():
    """
    Временный маршрут-заглушка для архива дел.
    """
    if not session.get('logged_in'):
        return redirect(url_for('bot_portal.login'))

    # Пока что просто отображаем заглушку
    return "<h1>Архив дел</h1><p>Эта страница находится в разработке.</p><a href='/bot/dashboard'>Назад</a>"
# --- КОНЕЦ ИЗМЕНЕНИЙ ---

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