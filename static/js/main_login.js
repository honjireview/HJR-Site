// static/js/main_login.js
document.addEventListener('DOMContentLoaded', () => {
    // --- Получаем все нужные элементы со страницы ---
    const userIcon = document.getElementById('user-icon');
    const overlay = document.getElementById('auth-modal-overlay');
    const modal = document.getElementById('auth-modal');

    // --- Проверяем, должны ли мы открыть окно при загрузке страницы ---
    const shouldOpenModalOnLoad = document.body.dataset.openLoginModal === 'true';

    // --- Проверяем, что все элементы на месте, чтобы избежать ошибок ---
    if (!userIcon || !overlay || !modal) {
        console.error('Не найдены все компоненты модального окна входа.');
        return;
    }

    // --- ФУНКЦИИ ---

    // Функция, которая ПОКАЗЫВАЕТ окно
    const showModal = () => {
        overlay.classList.remove('hidden');
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden'; // Блокируем прокрутку страницы
    };

    // Функция, которая ПРЯЧЕТ окно
    const hideModal = () => {
        overlay.classList.add('hidden');
        modal.classList.add('hidden');
        document.body.style.overflow = ''; // Возвращаем прокрутку
    };

    // --- ЛОГИКА РАБОТЫ С URL ---

    // 1. При клике на иконку пользователя
    userIcon.addEventListener('click', (e) => {
        e.preventDefault(); // Отменяем стандартный переход по ссылке
        const loginUrl = userIcon.getAttribute('href');

        // Если мы еще не на странице /login, меняем URL
        if (window.location.pathname !== loginUrl) {
            history.pushState({ isModalOpen: true }, '', loginUrl);
        }
        showModal(); // Показываем окно
    });

    // 2. При клике на темный фон (overlay) для закрытия
    overlay.addEventListener('click', () => {
        // Используем history.back() для возврата на предыдущую страницу в истории.
        // Это более правильный способ, чем вручную менять URL.
        history.back();
    });

    // 3. При нажатии на клавишу Escape для закрытия
    document.addEventListener('keydown', (e) => {
        if (e.key === "Escape" && !modal.classList.contains('hidden')) {
            history.back();
        }
    });

    // 4. При использовании кнопок "вперед/назад" в браузере
    window.addEventListener('popstate', (e) => {
        // Если в истории браузера состояние "окно открыто" - показываем его.
        // Иначе - прячем.
        if (e.state && e.state.isModalOpen) {
            showModal();
        } else {
            hideModal();
        }
    });

    // 5. Если мы загрузили страницу по прямой ссылке /login
    if (shouldOpenModalOnLoad) {
        // Заменяем текущую запись в истории, чтобы при нажатии "назад" пользователь
        // попал на главную, а не на пустую страницу.
        history.replaceState({ isModalOpen: true }, '', window.location.href);
        showModal();
    }
});