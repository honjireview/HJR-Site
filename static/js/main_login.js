// static/js/main_login.js
document.addEventListener('DOMContentLoaded', () => {
    // --- Получаем все нужные элементы со страницы ---
    const userIcon = document.getElementById('user-icon');
    const overlay = document.getElementById('auth-modal-overlay');
    const modal = document.getElementById('auth-modal');

    // --- Проверяем, что все элементы на месте, чтобы избежать ошибок ---
    if (!userIcon || !overlay || !modal) {
        console.error('Не найдены все компоненты модального окна входа.');
        return;
    }

    // --- ОСНОВНАЯ ЛОГИКА ---

    // Функция, которая ПОКАЗЫВАЕТ окно
    const showModal = () => {
        overlay.classList.remove('hidden');
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    };

    // Функция, которая ПРЯЧЕТ окно
    const hideModal = () => {
        overlay.classList.add('hidden');
        modal.classList.add('hidden');
        document.body.style.overflow = '';
    };

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
        // history.back() вернет нас на предыдущий URL в истории браузера.
        // Это правильный способ закрытия, так как он вызовет событие popstate.
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
        // Если в объекте состояния истории есть наш флаг modal: 'open',
        // значит, мы должны показать окно. Иначе - скрыть.
        if (e.state && e.state.modal === 'open') {
            showModal();
        } else {
            hideModal();
        }
    });

    // 4. Проверка при ПЕРВОНАЧАЛЬНОЙ загрузке страницы
    // Если пользователь зашел по прямой ссылке /login...
    if (document.body.dataset.openLoginModal === 'true') {
        const loginUrl = userIcon.getAttribute('href');
        // ...мы заменяем текущую запись в истории браузера.
        // Это нужно, чтобы при нажатии "назад" пользователь попал
        // на главную страницу, а не на тот сайт, откуда он перешел по ссылке.
        history.replaceState({ modal: 'open' }, '', loginUrl);
        showModal();
    }
});