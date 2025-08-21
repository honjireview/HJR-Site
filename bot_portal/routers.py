from flask import render_template
from . import bot_portal_bp

# Этот роут будет доступен по адресу /bot/dashboard
@bot_portal_bp.route('/dashboard')
def dashboard():
    """
    Обрабатывает главную страницу портала бота.
    """
    return render_template('dashboard.html')

# Здесь в будущем будут роуты для /archive, /tracker, /stats и т.д.