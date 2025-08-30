// static/js/main_login.js
document.addEventListener('DOMContentLoaded', () => {
    const userIcon = document.getElementById('user-icon');
    const overlay = document.getElementById('auth-modal-overlay');
    const modal = document.getElementById('auth-modal');
    const loginView = document.getElementById('login-view');
    const registerView = document.getElementById('register-view');
    const showRegisterBtn = document.getElementById('show-register-view');
    const showLoginBtn = document.getElementById('show-login-view');

    // Store the original path to return to it when the modal is closed
    let originalPath = window.location.pathname;

    // Проверяем, существуют ли все необходимые элементы
    if (!userIcon || !overlay || !modal || !loginView || !registerView || !showRegisterBtn || !showLoginBtn) {
        // Эта ошибка не должна появляться, если HTML корректен
        console.error('Auth modal elements not found on the page.');
        return;
    }

    const openModal = () => {
        originalPath = window.location.pathname; // Save the path right before opening
        const langCode = originalPath.split('/')[1] || 'ru'; // Extract lang_code from URL
        const loginUrl = `/${langCode}/login`;

        history.pushState(null, '', loginUrl); // Change URL
        overlay.classList.remove('hidden');
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden'; // Блокируем скролл страницы
    };

    const closeModal = () => {
        history.pushState(null, '', originalPath); // Change URL back
        overlay.classList.add('hidden');
        modal.classList.add('hidden');
        document.body.style.overflow = ''; // Возвращаем скролл
    };

    userIcon.addEventListener('click', (e) => {
        e.preventDefault(); // Отменяем стандартное поведение ссылки
        openModal();
    });

    overlay.addEventListener('click', closeModal);

    // Добавим закрытие по клавише Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === "Escape" && !modal.classList.contains('hidden')) {
            closeModal();
        }
    });

    showRegisterBtn.addEventListener('click', (e) => {
        e.preventDefault();
        loginView.classList.add('hidden');
        registerView.classList.remove('hidden');
    });

    showLoginBtn.addEventListener('click', (e) => {
        e.preventDefault();
        registerView.classList.add('hidden');
        loginView.classList.remove('hidden');
    });

    // Handle back/forward browser button navigation
    window.addEventListener('popstate', () => {
        // If the modal should be open on the /login page but isn't, open it.
        if (window.location.pathname.endsWith('/login') && modal.classList.contains('hidden')) {
            openModal();
        }
        // If the modal is open but the URL is not /login anymore, close it.
        else if (!window.location.pathname.endsWith('/login') && !modal.classList.contains('hidden')) {
            closeModal();
        }
    });
});