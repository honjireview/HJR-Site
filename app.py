from flask import Flask
import os
import db
import telebot
import logging # <-- Импортируем логирование

# --- НАЧАЛО ИЗМЕНЕНИЙ ---
# Базовая конфигурация логирования.
# В Railway логи будут автоматически перехватываться и отображаться.
logging.basicConfig(
    level=logging.DEBUG, # Устанавливаем уровень DEBUG для максимальной детализации
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
# --- КОНЕЦ ИЗМЕНЕНИЙ ---


def create_app():
    """
    Создает и настраивает экземпляр приложения Flask (паттерн Application Factory).
    """
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'a_very_secret_key_for_local_development_only')

    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    if TELEGRAM_TOKEN:
        try:
            temp_bot = telebot.TeleBot(TELEGRAM_TOKEN)
            bot_info = temp_bot.get_me()
            app.config['TELEGRAM_BOT_USERNAME'] = bot_info.username
            logging.info(f"Успешно получен username бота: @{bot_info.username}")
        except Exception as e:
            raise RuntimeError(f"Не удалось получить информацию о боте: {e}")
    else:
        raise RuntimeError("TELEGRAM_TOKEN не установлен в переменных окружения.")

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