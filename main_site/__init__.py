from flask import Blueprint

# 1. Создаем "блюпринт"
main_site_bp = Blueprint(
    'main_site',
    __name__,
    template_folder='../templates/main_site',
    static_folder='../static'
)

# 2. Импортируем роуты в самом конце, чтобы избежать циклических импортов
from . import routes