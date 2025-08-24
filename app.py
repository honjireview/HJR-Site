# app.py
from flask import Flask
import os
import db
import telebot # <--- 1. Импортируем telebot

def create_app():
    """
    Создает и настраивает экземпляр приложения Flask (паттерн Application Factory).
    """
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'a_very_secret_key_for_local_development_only')

    # --- НАЧАЛО ИЗМЕНЕНИЙ ---
    # Получаем токен и инициализируем временный экземпляр бота
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    if TELEGRAM_TOKEN:
        try:
            temp_bot = telebot.TeleBot(TELEGRAM_TOKEN)
            bot_info = temp_bot.get_me()
            # 2. Сохраняем username в конфигурацию приложения
            app.config['TELEGRAM_BOT_USERNAME'] = bot_info.username
        except Exception as e:
            # Если токен невалидный или нет сети, приложение не запустится
            # Это правильное поведение - мы сразу узнаем о проблеме
            raise RuntimeError(f"Could not get bot info from Telegram API: {e}")
    else:
        # Если токен не задан, мы не можем работать
        raise RuntimeError("TELEGRAM_TOKEN is not set in environment variables.")
    # --- КОНЕЦ ИЗМЕНЕНИЙ ---

    db.init_app(app)

    from main_site.routes import main_site_bp
    from bot_portal.routes import bot_portal_bp

    app.register_blueprint(main_site_bp)
    app.register_blueprint(bot_portal_bp, url_prefix='/bot')

    return app

# Эта часть нужна для Gunicorn на Railway
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)