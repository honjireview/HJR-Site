from flask import Blueprint

# --- ИЗМЕНЕНИЕ: Возвращаемся к стандартному Blueprint ---
main_site_bp = Blueprint(
    'main_site',
    __name__,
    template_folder='../templates/main_site',
    static_folder='../static'
)

# Импортируем роуты в самом конце
from . import routes