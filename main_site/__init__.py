from flask import Blueprint, g, request
from werkzeug.routing import Rule

# --- НАЧАЛО ИЗМЕНЕНИЙ: Создаем собственный класс Blueprint ---
class I18nBlueprint(Blueprint):
    def __init__(self, name, import_name, **kwargs):
        super(I18nBlueprint, self).__init__(name, import_name, **kwargs)
        self.add_url_rule('/<lang_code>/', endpoint='index', view_func=lambda lang_code: None)

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        # Добавляем префикс /<lang_code> ко всем правилам, кроме статики
        if rule.startswith('/static/'):
            super(I18nBlueprint, self).add_url_rule(rule, endpoint, view_func, **options)
        else:
            # Создаем новое правило с языковым префиксом
            lang_rule = f'/<lang_code>{rule}'
            super(I18nBlueprint, self).add_url_rule(lang_rule, endpoint, view_func, **options)

    def register(self, app, options):
        # Эта функция будет вызываться при регистрации блюпринта
        @app.url_value_preprocessor
        def pull_lang_code(endpoint, values):
            if endpoint and endpoint.startswith(self.name):
                g.lang_code = values.pop('lang_code', None)

        @app.url_defaults
        def add_language_code(endpoint, values):
            if 'lang_code' in values or not g.get('lang_code'):
                return
            if endpoint.startswith(self.name):
                values['lang_code'] = g.lang_code

        super(I18nBlueprint, self).register(app, options)

# Создаем блюпринт, используя наш новый класс
main_site_bp = I18nBlueprint(
    'main_site',
    __name__,
    template_folder='../templates/main_site',
    static_folder='../static'
)
# --- КОНЕЦ ИЗМЕНЕНИЙ ---

from . import routes