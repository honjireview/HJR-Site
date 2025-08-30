// static/js/main_login.js
document.addEventListener('DOMContentLoaded', () => {
    const userIcon = document.getElementById('user-icon');
    const overlay = document.getElementById('auth-modal-overlay');
    const modal = document.getElementById('auth-modal');
    const loginView = document.getElementById('login-view');
    const registerView = document.getElementById('register-view');
    const showRegisterBtn = document.getElementById('show-register-view');
    const showLoginBtn = document.getElementById('show-login-view');

    let originalPath = window.location.pathname;

    if (!userIcon || !overlay || !modal || !loginView || !registerView || !showRegisterBtn || !showLoginBtn) {
        console.error('Auth modal elements not found on the page.');
        return;
    }

    const openModal = () => {
        originalPath = window.location.pathname;
        const loginUrl = userIcon.getAttribute('href'); // Получаем URL напрямую из ссылки

        // Используем replaceState, чтобы не создавать лишнюю запись в истории
        history.replaceState({ modal: 'open' }, '', loginUrl);

        overlay.classList.remove('hidden');
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    };

    const closeModal = () => {
        // Возвращаемся на исходный URL
        history.replaceState({ modal: 'closed' }, '', originalPath);

        overlay.classList.add('hidden');
        modal.classList.add('hidden');
        document.body.style.overflow = '';
    };

    userIcon.addEventListener('click', (e) => {
        e.preventDefault();
        openModal();
    });

    overlay.addEventListener('click', closeModal);

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

    // Обработка кнопок "назад/вперед" в браузере
    window.addEventListener('popstate', () => {
        const currentPath = window.location.pathname;
        if (currentPath.endsWith('/login') && modal.classList.contains('hidden')) {
            openModal();
        } else if (!currentPath.endsWith('/login') && !modal.classList.contains('hidden')) {
            closeModal();
        }
    });
});