# passenger_wsgi.py
import sys
import os

# Добавляем путь к проекту в системные пути Python
sys.path.insert(0, os.path.dirname(__file__))

# Импортируем главный объект приложения из вашего app.py
from app import app as application