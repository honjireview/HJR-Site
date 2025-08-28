from flask import Flask
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
import os
import db
import telebot
import logging
import subprocess
from datetime import timedelta

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def get_git_commit_hash():
    try:
        commit_hash = os.getenv('RAILWAY_GIT_COMMIT_SHA') or os.getenv('COMMIT_HASH')
        if commit_hash:
            return commit_hash[:7]

        commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip().decode('utf-8')
        return commit_hash
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def create_app():
    app = Flask(__name__)

    # --- ОКОНЧАТЕЛЬНОЕ ИСПРАВЛЕНИЕ, КОТОРОЕ РЕШАЕТ ВСЮ ПРОБЛЕМУ ---
    # Эта конфигурация Talisman РАЗРЕШАЕТ загрузку необходимых скриптов и стилей.
    csp = {
        'default-src': '\'self\'',
        'script-src': [
            '\'self\'',
            'https://cdn.tailwindcss.com',  # Разрешает скрипт Tailwind
            'https://telegram.org'
        ],
        'style-src': [
            '\'self\'',
            '\'unsafe-inline\'',  # Необходимо для работы Tailwind JIT
            'https://cdn.tailwindcss.com',
            'https://fonts.googleapis.com' # Разрешает стили Google Fonts
        ],
        'font-src': [
            '\'self\'',
            'https://fonts.gstatic.com' # Разрешает сами файлы шрифтов
        ],
        'img-src': [
            '\'self\'',
            'data:',
            'https:'
        ],
        'frame-src': ['https://oauth.telegram.org', 'https://telegram.org']
    }
    Talisman(app, content_security_policy=csp)
    # --- КОНЕЦ ИСПРАВЛЕНИЯ ---

    csrf = CSRFProtect(app)
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'a_very_secret_key_for_local_development_only')
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
    app.config['COMMIT_HASH'] = get_git_commit_hash() or 'local'

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

    from main_site import main_site_bp
    from bot_portal import bot_portal_bp
    from bot_portal.logs_routes import logs_bp

    app.register_blueprint(main_site_bp)
    app.register_blueprint(bot_portal_bp, url_prefix='/bot')
    app.register_blueprint(logs_bp, url_prefix='/bot/admin')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)