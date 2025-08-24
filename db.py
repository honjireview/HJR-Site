# db.py
import os
import psycopg2
from flask import g

def get_db():
    """
    Открывает новое соединение с БД, если его еще нет для текущего запроса.
    """
    if 'db' not in g:
        g.db = psycopg2.connect(os.getenv("DATABASE_URL"))
    return g.db

def close_db(e=None):
    """
    Закрывает соединение с БД, если оно было установлено.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    """
    Регистрирует функции управления БД в приложении Flask.
    """
    app.teardown_appcontext(close_db)