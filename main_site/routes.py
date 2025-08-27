from flask import render_template
from . import main_site_bp
from bot_portal.models.editor_model import EditorModel


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
    Обрабатывает страницу "О нас", загружая список редакторов из БД.
    """
    all_editors = EditorModel.get_all_editors()
    executor = next((editor for editor in all_editors if editor['role'] == 'executor'), None)
    editors = [editor for editor in all_editors if editor['role'] != 'executor']
    return render_template('about.html', executor=executor, editors=editors)

@main_site_bp.route('/privacy-policy')
def privacy_policy():
    """
    Обрабатывает страницу политики конфиденциальности.
    """
    return render_template('privacy_policy.html')