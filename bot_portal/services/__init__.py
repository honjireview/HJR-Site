# /bot_portal/services/__init__.py

# Этот файл делает директорию 'services' пакетом Python.
# Мы импортируем классы сюда, чтобы сделать
# импорты в других частях приложения короче и чище.

from .auth_service import AuthService
from .appeal_service import AppealService
from .gemini_service import GeminiService