from flask import Blueprint

# 1. Создаем "блюпринт"
bot_portal_bp = Blueprint(
    'bot_portal',
    __name__,
    template_folder='../templates/bot_portal'
)

# 2. Импортируем роуты в самом конце, чтобы избежать циклических импортов
from . import routes