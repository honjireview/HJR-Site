from flask import render_template
from . import main_site_bp

@main_site_bp.route('/')
def index():
    """
    Обрабатывает главную страницу сайта.
    """
    # render_template будет искать 'index.html' в папке,
    # которую мы указали в __init__.py (templates/main_site)
    return render_template('index.html')

@main_site_bp.route('/contact')
def contact():
    """
    Обрабатывает страницу контактов.
    """
    return render_template('contact.html')

# Здесь в будущем будут роуты для форума, отзывов и т.д.