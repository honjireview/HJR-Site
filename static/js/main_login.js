// static/js/main_login.js
document.addEventListener('DOMContentLoaded', () => {
    const userIcon = document.getElementById('user-icon');
    const overlay = document.getElementById('auth-modal-overlay');
    const modal = document.getElementById('auth-modal');

    // Проверяем, что все элементы существуют
    if (!userIcon || !overlay || !modal) {
        console.error('Не найдены все компоненты модального окна входа.');
        return;
    }

    // --- ФУНКЦИИ УПРАВЛЕНИЯ ОКНОМ ---
    const showModal = () => {
        overlay.classList.remove('hidden');
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden'; // Блокируем прокрутку
    };

    const hideModal = () => {
        overlay.classList.add('hidden');
        modal.classList.add('hidden');
        document.body.style.overflow = ''; // Возвращаем прокрутку
    };

    // --- ЛОГИКА ---

    // 1. Открытие окна по клику на иконку
    userIcon.addEventListener('click', (e) => {
        e.preventDefault(); // Отменяем стандартный переход по ссылке
        const loginUrl = userIcon.getAttribute('href');

        // Добавляем запись в историю браузера и меняем URL
        history.pushState({ modal: 'open' }, '', loginUrl);
        showModal(); // Показываем окно
    });

    // 2. Закрытие окна (клик на фон или Escape)
    const closeModal = () => {
        // history.back() вернет нас на предыдущий URL
        history.back();
    };
    overlay.addEventListener('click', closeModal);
    document.addEventListener('keydown', (e) => {
        if (e.key === "Escape" && !modal.classList.contains('hidden')) {
            closeModal();
        }
    });

    // 3. Обработка кнопок "вперед/назад" в браузере
    window.addEventListener('popstate', (e) => {
        const loginUrl = userIcon.getAttribute('href');
        // Проверяем, соответствует ли текущий URL - URLу для логина
        if (window.location.href === loginUrl) {
            showModal(); // Если да, показываем окно
        } else {
            hideModal(); // Если нет, прячем
        }
    });

    // 4. Проверка при ПЕРВОЙ загрузке страницы
    // Если пользователь зашел по прямой ссылке /login...
    if (document.body.dataset.openLoginModal === 'true') {
        const loginUrl = userIcon.getAttribute('href');
        // ...мы заменяем текущую (первую) запись в истории браузера.
        // Это нужно, чтобы при нажатии "назад" пользователь попал
        // на главную страницу, а не на тот сайт, откуда он перешел по ссылке.
        history.replaceState({ modal: 'open' }, '', loginUrl);
        showModal();
    }
});