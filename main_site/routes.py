# /bot_portal/routes.py
from flask import render_template, request, redirect, url_for, session, current_app # <--- Импортируем current_app
# ... (остальные импорты)

# ... (dashboard, handle_login, logout)

@bot_portal_bp.route('/login')
def login():
    """
    Отображает страницу входа.
    """
    # 3. Получаем username из конфигурации, а не из os.getenv
    bot_username = current_app.config.get('TELEGRAM_BOT_USERNAME', 'YourBot')
    return render_template('login.html', bot_username=bot_username)