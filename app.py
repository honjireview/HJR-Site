from flask import Flask
import os

def create_app():
    """
    Создает и настраивает экземпляр приложения Flask (паттерн Application Factory).
    """
    app = Flask(__name__)

    # Настройка секретного ключа для сессий (важно для авторизации)
    # В Railway эту переменную нужно будет добавить в окружение
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'a_default_secret_key_for_local_dev')

    # Здесь в будущем будет логика подключения к базе данных
    # ...

    # Регистрация "блюпринтов" (наших мини-приложений)
    from main_site.routes import main_site_bp
    from bot_portal.routes import bot_portal_bp

    app.register_blueprint(main_site_bp)
    # Все URL-адреса портала бота будут начинаться с /bot/ (например, /bot/archive)
    app.register_blueprint(bot_portal_bp, url_prefix='/bot')

    return app

# Эта часть нужна для Gunicorn на Railway
app = create_app()

if __name__ == '__main__':
    # Запускаем для локальной разработки.
    app.run(debug=True, port=5000)