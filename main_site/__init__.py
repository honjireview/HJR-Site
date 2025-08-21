from flask import Blueprint

# Создаем "блюпринт" для основного сайта.
# Это позволяет нам организовать роуты в отдельном модуле.
main_site_bp = Blueprint(
    'main_site',
    __name__,
    template_folder='../templates/main_site', # Указываем, где лежат HTML-шаблоны
    static_folder='../static' # Указываем, где лежат CSS/JS
)

# Импортируем роуты в конце, чтобы избежать циклических зависимостей
from . import routes