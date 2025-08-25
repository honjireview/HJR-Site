from flask import render_template
from . import main_site_bp

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

@main_site_bp.route('/about')
def about():
    """
    Обрабатывает страницу "О нас".
    """
    return render_template('about.html')