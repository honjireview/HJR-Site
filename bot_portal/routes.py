# /bot_portal/routes.py
from flask import render_template, request, redirect, url_for, session, current_app
import os
from . import bot_portal_bp
from .services import AuthService, AppealService

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
    Отображает страницу с архивом всех дел.
    """
    if not session.get('logged_in'):
        return redirect(url_for('bot_portal.login'))

    # Получаем отформатированные данные через сервис
    appeals_list = AppealService.get_all_appeals_for_display()

    # Передаем данные в новый шаблон
    return render_template('archive.html', appeals=appeals_list)

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
        # В реальной системе здесь может быть страница с ошибкой
        return f"Ошибка авторизации: {message}", 403

@bot_portal_bp.route('/logout')
def logout():
    """
    Выход из системы.
    """
    AuthService.logout_user()
    return redirect(url_for('bot_portal.showcase'))