from flask import Blueprint

main_site_bp = Blueprint(
    'main_site',
    __name__,
    template_folder='../templates/main_site',
    static_folder='../static'
)

# --- ИЗМЕНЕНИЕ: Строка "from . import routes" удалена отсюда ---