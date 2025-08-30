// static/js/main_login.js
document.addEventListener('DOMContentLoaded', () => {
    const userIcon = document.getElementById('user-icon');
    const overlay = document.getElementById('auth-modal-overlay');
    const modal = document.getElementById('auth-modal');
    const loginView = document.getElementById('login-view');
    const registerView = document.getElementById('register-view');
    const showRegisterBtn = document.getElementById('show-register-view');
    const showLoginBtn = document.getElementById('show-login-view');

    // Проверяем, передал ли Flask флаг для открытия окна
    const shouldOpenModalOnLoad = document.body.dataset.openLoginModal === 'true';

    // Определяем "домашний" URL, на который нужно будет вернуться
    // Если мы уже на /login, то "дом" - это /<lang_code>/. Иначе - текущий URL.
    const homePath = window.location.pathname.endsWith('/login')
        ? window.location.pathname.substring(0, window.location.pathname.lastIndexOf('/')) + '/'
        : window.location.pathname;

    if (!userIcon || !overlay || !modal || !loginView || !registerView || !showRegisterBtn || !showLoginBtn) {
        console.error('Auth modal elements not found on the page.');
        return;
    }

    const openModal = () => {
        const loginUrl = userIcon.getAttribute('href');

        // Меняем URL, только если он еще не /login
        if (window.location.pathname !== loginUrl) {
            // pushState добавляет новую запись в историю браузера
            history.pushState({ modalOpen: true }, '', loginUrl);
        }

        overlay.classList.remove('hidden');
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    };

    const closeModal = () => {
        // Возвращаемся на предыдущий URL
        if (window.location.pathname.endsWith('/login')) {
            history.pushState({ modalOpen: false }, '', homePath);
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

    // Слушаем кнопки "вперед/назад" в браузере
    window.addEventListener('popstate', () => {
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

    // Если сервер сказал открыть окно при загрузке - открываем
    if (shouldOpenModalOnLoad) {
        openModal();
    }
});