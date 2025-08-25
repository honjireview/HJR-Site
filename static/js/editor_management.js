document.addEventListener('DOMContentLoaded', () => {
    const toggleButtons = document.querySelectorAll('.status-toggle-btn');

    toggleButtons.forEach(button => {
        button.addEventListener('click', async () => {
            const userId = button.dataset.userId;
            const currentIsInactive = button.dataset.isInactive === 'true';
            const newIsInactive = !currentIsInactive;

            // Блокируем кнопку, чтобы избежать двойных нажатий
            button.disabled = true;
            button.textContent = 'Обновляю...';

            try {
                const response = await fetch('/bot/editors/update-status', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        user_id: userId,
                        is_inactive: newIsInactive
                    }),
                });

                const result = await response.json();

                if (result.success) {
                    // Обновляем UI без перезагрузки страницы
                    updateRow(userId, newIsInactive);
                } else {
                    alert('Ошибка: ' + (result.error || 'Не удалось обновить статус.'));
                    // Возвращаем кнопке исходное состояние
                    button.textContent = newIsInactive ? 'Отправить в СНС' : 'Сделать активным';
                }

            } catch (error) {
                console.error('Ошибка сети:', error);
                alert('Произошла ошибка сети. Попробуйте еще раз.');
                button.textContent = newIsInactive ? 'Отправить в СНС' : 'Сделать активным';
            } finally {
                // Разблокируем кнопку в любом случае
                button.disabled = false;
            }
        });
    });

    function updateRow(userId, isInactive) {
        const row = document.getElementById(`editor-row-${userId}`);
        if (!row) return;

        const statusText = row.querySelector('.status-text');
        const button = row.querySelector('.status-toggle-btn');

        // Обновляем текст статуса
        if (isInactive) {
            statusText.className = 'status-text px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-500/20 text-yellow-300';
            statusText.textContent = 'В СНС';
        } else {
            statusText.className = 'status-text px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-500/20 text-green-300';
            statusText.textContent = 'Активен';
        }

        // Обновляем кнопку
        button.dataset.isInactive = isInactive.toString();
        button.textContent = isInactive ? 'Сделать активным' : 'Отправить в СНС';
    }
});