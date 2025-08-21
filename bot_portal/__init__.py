from flask import Blueprint

# Создаем "блюпринт" для портала бота.
bot_portal_bp = Blueprint(
    'bot_portal',
    __name__,
    template_folder='../templates/bot_portal',
    static_folder='../static'
)

from . import routes