from flask import Flask
import os
import db
import telebot
import logging
import subprocess

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def get_git_commit_hash():
    try:
        commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip().decode('utf-8')
        return commit_hash
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'a_very_secret_key_for_local_development_only')

    commit_hash = os.getenv('COMMIT_HASH') or get_git_commit_hash()
    app.config['COMMIT_HASH'] = commit_hash or 'local'

    HJRBOT_TELEGRAM_TOKEN = os.getenv('HJRBOT_TELEGRAM_TOKEN')
    if HJRBOT_TELEGRAM_TOKEN:
        try:
            temp_bot = telebot.TeleBot(HJRBOT_TELEGRAM_TOKEN)
            bot_info = temp_bot.get_me()
            app.config['TELEGRAM_BOT_USERNAME'] = bot_info.username
            logging.info(f"Успешно получен username бота: @{bot_info.username}")
        except Exception as e:
            raise RuntimeError(f"Не удалось получить информацию о боте: {e}")
    else:
        raise RuntimeError("HJRBOT_TELEGRAM_TOKEN не установлен в переменных окружения.")

    with app.app_context():
        db.init_db_schema()

    db.init_app(app)

    # --- НАЧАЛО ИЗМЕНЕНИЙ: Структура импортов переработана ---

    # 1. Сначала импортируем только блюпринты
    from main_site import main_site_bp
    from bot_portal import bot_portal_bp
    from bot_portal.logs_routes import logs_bp

    # 2. Регистрируем их в приложении
    app.register_blueprint(main_site_bp)
    app.register_blueprint(bot_portal_bp, url_prefix='/bot')
    app.register_blueprint(logs_bp, url_prefix='/bot/admin')

    # 3. И только теперь, когда все готово, импортируем роуты.
    # Это гарантирует, что все зависимости (app, bp) уже существуют.
    with app.app_context():
        from main_site import routes
        from bot_portal import routes

    # --- КОНЕЦ ИЗМЕНЕНИЙ ---

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)