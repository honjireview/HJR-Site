from flask import Blueprint

bot_portal_bp = Blueprint(
    'bot_portal',
    __name__,
    template_folder='../templates/bot_portal'
)

# --- ИЗМЕНЕНИЕ: Строка "from . import routes" удалена отсюда ---