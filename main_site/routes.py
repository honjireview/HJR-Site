# /main_site/routes.py
from flask import render_template
# --- НАЧАЛО ИЗМЕНЕНИЙ: Импортируем блюпринт из __init__.py ---
from . import main_site_bp
# --- КОНЕЦ ИЗМЕНЕНИЙ ---

@main_site_bp.route('/')
def index():
    """
    Обрабатывает главную страницу основного сайта.
    """
    return render_template('index.html')

@main_site_bp.route('/contact')
def contact():
    """
    Обрабатывает страницу контактов.
    """
    return render_template('contact.html')