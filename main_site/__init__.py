from flask import Blueprint

# Blueprint для динамических, языковых маршрутов
main_site_bp = Blueprint(
    'main_site',
    __name__,
    template_folder='../templates/main_site'
)

# ОТДЕЛЬНЫЙ Blueprint только для статических файлов.
# У него нет языкового префикса.
static_bp = Blueprint(
    'main_site_static',
    __name__,
    static_folder='../static',
    static_url_path='/main_site/static'
)

from . import routes