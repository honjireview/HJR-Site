from flask import Flask, redirect, url_for, request, g, session
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from flask_babel import Babel
import os
import db
import telebot
import logging
import subprocess
from datetime import timedelta

LANGUAGES = ['ru', 'en']
babel = Babel()

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

    csp = {
        'default-src': [
            '\'self\'',
            'http://www.w3.org/2000/svg'
        ],
        'script-src': [
            '\'self\'',
            'https://cdn.tailwindcss.com',
            'https://telegram.org',
            '//unpkg.com/alpinejs' # Добавлено для AlpineJS
        ],
        'style-src': [
            '\'self\'',
            '\'unsafe-inline\'',
            'https://cdn.tailwindcss.com',
            'https://fonts.googleapis.com'
        ],
        'font-src': [
            '\'self\'',
            'https://fonts.gstatic.com'
        ],
        'img-src': [
            '\'self\'',
            'data:',
            'https:'
        ],
        'frame-src': ['https://oauth.telegram.org', 'https://telegram.org']
    }
    Talisman(app, content_security_policy=csp)

    csrf = CSRFProtect(app)
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'a_very_secret_key_for_local_development_only')
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
    app.config['COMMIT_HASH'] = get_git_commit_hash() or 'local'
    app.config['BABEL_DEFAULT_LOCALE'] = 'ru'
    babel.init_app(app)

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

    app.register_blueprint(main_site_bp, url_prefix='/<lang_code>')
    app.register_blueprint(bot_portal_bp, url_prefix='/bot')
    app.register_blueprint(logs_bp, url_prefix='/bot/admin')

    @babel.localeselector
    def get_locale():
        # Язык теперь всегда берется из URL
        if g.get('lang_code') in LANGUAGES:
            return g.lang_code
        # Если в URL нет валидного языка, используем язык браузера или по умолчанию
        return request.accept_languages.best_match(LANGUAGES) or 'ru'

    @app.url_defaults
    def add_language_code(endpoint, values):
        if 'lang_code' not in values and g.get('lang_code'):
            if app.url_map.is_endpoint_prefixed(endpoint, 'main_site'):
                values['lang_code'] = g.lang_code

    @app.url_value_preprocessor
    def pull_lang_code(endpoint, values):
        g.lang_code = values.pop('lang_code', None) if values else None

    @app.before_request
    def before_request_locale():
        if request.endpoint and 'lang_code' not in request.view_args:
            g.lang_code = get_locale()

    # --- ИЗМЕНЕНИЕ: Главная страница теперь всегда редиректит на URL с префиксом /ru ---
    @app.route('/')
    def root_redirect():
        # Определяем лучший язык для первого визита и редиректим на него
        best_lang = request.accept_languages.best_match(LANGUAGES) or 'ru'
        return redirect(url_for('main_site.index', lang_code=best_lang))
    # --- КОНЕЦ ИЗМЕНЕНИЙ ---

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)