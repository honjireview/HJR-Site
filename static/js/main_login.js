// static/js/main_login.js
document.addEventListener('DOMContentLoaded', () => {
    const userIcon = document.getElementById('user-icon');
    const overlay = document.getElementById('auth-modal-overlay');
    const modal = document.getElementById('auth-modal');
    const loginView = document.getElementById('login-view');
    const registerView = document.getElementById('register-view');
    const showRegisterBtn = document.getElementById('show-register-view');
    const showLoginBtn = document.getElementById('show-login-view');

    // Проверяем, существуют ли все необходимые элементы
    if (!userIcon || !overlay || !modal || !loginView || !registerView || !showRegisterBtn || !showLoginBtn) {
        // Эта ошибка не должна появляться, если HTML корректен
        console.error('Auth modal elements not found on the page.');
        return;
    }

    const openModal = () => {
        overlay.classList.remove('hidden');
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden'; // Блокируем скролл страницы
    };

    const closeModal = () => {
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
});