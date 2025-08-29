from flask import Blueprint, g

# --- ИЗМЕНЕНИЕ: Упрощаем класс Blueprint ---
class I18nBlueprint(Blueprint):
    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        # Добавляем префикс /<lang_code> ко всем правилам
        prefixed_rule = f'/<lang_code>{rule}'
        super().add_url_rule(prefixed_rule, endpoint, view_func, **options)

# Создаем блюпринт, используя наш новый класс
main_site_bp = I18nBlueprint(
    'main_site',
    __name__,
    template_folder='../templates/main_site',
    static_folder='../static'
)

# --- ИЗМЕНЕНИЕ: Переносим логику обработки URL сюда ---
@main_site_bp.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code', None)

@main_site_bp.url_defaults
def add_language_code(endpoint, values):
    if 'lang_code' in values or not hasattr(g, 'lang_code'):
        return
    if main_site_bp.app.url_map.is_endpoint_prefixed(endpoint, main_site_bp.name):
        values['lang_code'] = g.lang_code
# --- КОНЕЦ ИЗМЕНЕНИЙ ---


from . import routes