// static/js/main_login.js
document.addEventListener('DOMContentLoaded', () => {
    const userIcon = document.getElementById('user-icon');
    const overlay = document.getElementById('auth-modal-overlay');
    const modal = document.getElementById('auth-modal');
    const loginView = document.getElementById('login-view');
    const registerView = document.getElementById('register-view');
    const showRegisterBtn = document.getElementById('show-register-view');
    const showLoginBtn = document.getElementById('show-login-view');

    // Флаг, который мы передаем из Flask (`open_login_modal`)
    // Проверяем, есть ли на странице элемент, который мы создадим при open_login_modal=True
    const shouldOpenModal = document.body.dataset.openLoginModal === 'true';

    let originalPath = window.location.pathname.endsWith('/login')
        ? `/${window.location.pathname.split('/')[1]}` // Если мы на /login, то "домой" - это /ru/
        : window.location.pathname;

    if (!userIcon || !overlay || !modal || !loginView || !registerView || !showRegisterBtn || !showLoginBtn) {
        console.error('Auth modal elements not found on the page.');
        return;
    }

    const openModal = () => {
        const loginUrl = userIcon.getAttribute('href');

        // Меняем URL, только если он еще не изменен
        if (window.location.pathname !== loginUrl) {
            history.pushState({ modal: 'open' }, '', loginUrl);
        }

        overlay.classList.remove('hidden');
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    };

    const closeModal = () => {
        // Возвращаемся на исходный URL, если мы на странице /login
        if (window.location.pathname.endsWith('/login')) {
            history.pushState({ modal: 'closed' }, '', originalPath);
        }

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
    window.addEventListener('popstate', (event) => {
        if (window.location.pathname.endsWith('/login')) {
            if (modal.classList.contains('hidden')) {
                openModal();
            }
        } else {
            if (!modal.classList.contains('hidden')) {
                closeModal();
            }
        }
    });

    // Если страница загрузилась с флагом от Flask, открываем окно
    if (shouldOpenModal) {
        openModal();
    }
});