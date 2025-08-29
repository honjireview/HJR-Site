# main_site/routes.py
from flask import render_template, redirect, url_for
from . import main_site_bp
from bot_portal.models.editor_model import EditorModel


@main_site_bp.route('/')
def index():
    """
    Обрабатывает главную страницу основного сайта.
    """
    # Временные данные для демонстрации дизайна
    latest_reviews = [
        {
            "date": "14.04.2025",
            "title": "“Злой король” — трон из лжи, корона из ада",
            "description": "Мрачная и увлекательная история о магии, борьбе за власть и сложных отношениях, где каждая сила имеет свою цену."
        },
        {
            "date": "12.04.2025",
            "title": "“Жестокий принц” — игра теней, сердце в броне, корона в шипах",
            "description": "История о хрупкой смертной, чьи амбиции опаснее магии, и о принце фейри, для которого презрение — искусство, и чья магия питается кровью и гордостью."
        },
        {
            "date": "10.04.2025",
            "title": "“Преступление и наказание” — хроника внутреннего мрака и тревожной совести",
            "description": "Роман о границах морали, страхе, вине и пути к искуплению в мире, где истина не всегда светла."
        }
    ]
    return render_template('main_site/index.html', latest_reviews=latest_reviews)


@main_site_bp.route('/community')
def discussed():
    """
    Обрабатывает страницу каталога "Обсуждаемое".
    """
    # Временные данные из скриншота
    discussed_reviews = [
        {
            "tag": "Популярное",
            "tag_style": "gradient", # Стиль для тега
            "title": "“Злой король” — трон из лжи, корона из яда",
            "description": "Мрачная и увлекательная история о магии, борьбе за власть и сложных отношениях, где каждая сила имеет свою цену.",
            "date": "24.04.2025",
            "image": "https://cv2.litres.ru/pub/c/pdf-kniga/pages/66710427/p1000.jpg"
        },
        {
            "tag": "Популярное",
            "tag_style": "gradient",
            "title": "«Вкус корней» — зов земли, горечь памяти и шепот прошлого",
            "description": "Сборник изящных афоризмов о добродетели, страстях и природе человека, в котором древняя мудрость прорастает сквозь повседневность, как корни сквозь камень.",
            "date": "12.04.2025",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_p_G5ECI2429i2LpB-4daAUNq2oQZ-3G7-A&s"
        },
        {
            "tag": "Популярное",
            "tag_style": "gradient",
            "title": "«Магическая битва» — проклятие в крови, воля сильнее смерти",
            "description": "Мир, где магия питается болью, чудовища живут в людях, а выживают только те, кто смотрит страху прямо в глаза.",
            "date": "22.04.2025",
            "image": "https://m.media-amazon.com/images/I/815uG5t4YVL._AC_UF1000,1000_QL80_.jpg"
        }
    ]
    return render_template('main_site/catalog.html',
                           page_title="Обсуждаемое",
                           reviews=discussed_reviews)


@main_site_bp.route('/reviews')
def reviews():
    """
    Обрабатывает страницу каталога "Рецензии".
    """
    reviews_data = [
        {
            "tag": "Новая рецензия",
            "tag_style": "purple", # Другой стиль для тега
            "title": "«Магическая битва» — проклятие в крови, воля сильнее смерти",
            "description": "Мир, где магия питается болью, чудовища живут в людях, а выживают только те, кто смотрит страху прямо в глаза.",
            "date": "22.04.2025",
            "image": "https://m.media-amazon.com/images/I/815uG5t4YVL._AC_UF1000,1000_QL80_.jpg"
        }
    ]
    return render_template('main_site/catalog.html',
                           page_title="Рецензии",
                           reviews=reviews_data)


@main_site_bp.route('/new')
def new_reviews():
    """
    Обрабатывает страницу каталога "Новые".
    """
    new_reviews_data = [
        {
            "tag": "Новый отзыв",
            "tag_style": "gradient",
            "title": "«Маленький принц» — нежная притча о дружбе, одиночестве и смысле жизни.",
            "description": "Мир глазами ребёнка, где укрощённый лис важнее короля, а простая фраза меняет Вселенную.",
            "date": "24.04.2025",
            "image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1367528355l/157993.jpg"
        },
        {
            "tag": "Новый отзыв",
            "tag_style": "gradient",
            "title": "«Жестокий принц» — сердце в броне, корона в шипах",
            "description": "История о хрупкой смертной, чьи амбиции опаснее магии, а чувства легко превращаются в оружие.",
            "date": "12.04.2025",
            "image": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1529520409l/25437156._SY475_.jpg"
        },
        {
            "tag": "Новая рецензия",
            "tag_style": "purple",
            "title": "«Преступление и наказание» — хроника внутреннего мрака и тревожной совести",
            "description": "Роман о границах морали, страхе, вине и пути к искуплению в мире, где истина не всегда светла.",
            "date": "22.04.2025",
            "image": "https://img4.labirint.ru/rc/6dc2a118e3322123512e0964205a1e75/220x340/books29/281358/cover.jpg?1563544474"
        }
    ]
    return render_template('main_site/catalog.html',
                           page_title="Новые",
                           reviews=new_reviews_data)


@main_site_bp.route('/about')
def about():
    """
    Обрабатывает страницу "О нас", загружая список редакторов из БД.
    """
    all_editors = EditorModel.get_all_editors()
    executor = next((editor for editor in all_editors if editor.get('role') == 'executor'), None)
    editors = [editor for editor in all_editors if editor.get('role') != 'executor']
    return render_template('main_site/about.html', executor=executor, editors=editors)


@main_site_bp.route('/privacy-policy')
def privacy_policy():
    """
    Обрабатывает страницу политики конфиденциальности.
    """
    return render_template('main_site/privacy_policy.html')

@main_site_bp.route('/licenses')
def licenses():
    """
    Отображает страницу с информацией о лицензиях и благодарностями.
    """
    return render_template('main_site/licenses.html')

@main_site_bp.route('/disclaimer')
def disclaimer():
    """
    Отображает страницу "Отказ от ответственности".
    """
    return render_template('main_site/disclaimer.html')

@main_site_bp.route('/community-rules')
def community_rules():
    """
    Отображает страницу "Правила сообщества".
    """
    return render_template('main_site/community_rules.html')

@main_site_bp.route('/login')
def login():
    """
    Резервный маршрут для страницы входа.
    """
    return redirect(url_for('main_site.index'))