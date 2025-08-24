# /main_site/routes.py
from flask import render_template
from . import main_site_bp

@main_site_bp.route('/')
def index():
    """
    Обрабатывает главную страницу основного сайта.
    """
    # Этот маршрут теперь будет отображать заглушку или главную страницу всего проекта,
    # так как витрина бота была перенесена.
    return render_template('index.html')

@main_site_bp.route('/contact')
def contact():
    """
    Обрабатывает страницу контактов.
    """
    return render_template('contact.html')