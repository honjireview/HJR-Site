from flask import render_template
from . import main_site_bp
from bot_portal.models.editor_model import EditorModel


@main_site_bp.route('/')
def index():
    """
    Обрабатывает главную страницу основного сайта.
    """
    # Временные данные для демонстрации дизайна
    latest_reviews = [
        {
            "date": "14.04.2025",
            "title": "“Злой король” — трон из лжи, корона из ада",
            "description": "Мрачная и увлекательная история о магии, борьбе за власть и сложных отношениях, где каждая сила имеет свою цену."
        },
        {
            "date": "12.04.2025",
            "title": "“Жестокий принц” — игра теней, сердце в броне, корона в шипах",
            "description": "История о хрупкой смертной, чьи амбиции опаснее магии, и о принце фейри, для которого презрение — искусство, и чья магия питается кровью и гордостью."
        },
        {
            "date": "10.04.2025",
            "title": "“Преступление и наказание” — хроника внутреннего мрака и тревожной совести",
            "description": "Роман о границах морали, страхе, вине и пути к искуплению в мире, где истина не всегда светла."
        }
    ]
    return render_template('index.html', latest_reviews=latest_reviews)


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
    executor = next((editor for editor in all_editors if editor.get('role') == 'executor'), None)
    editors = [editor for editor in all_editors if editor.get('role') != 'executor']
    return render_template('about.html', executor=executor, editors=editors)


@main_site_bp.route('/privacy-policy')
def privacy_policy():
    """
    Обрабатывает страницу политики конфиденциальности.
    """
    return render_template('privacy_policy.html')