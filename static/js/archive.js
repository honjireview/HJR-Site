document.addEventListener('DOMContentLoaded', () => {
    // Находим все строки в таблице, у которых есть атрибут 'data-href'
    const rows = document.querySelectorAll('tr[data-href]');

    // Для каждой такой строки добавляем обработчик клика
    rows.forEach(row => {
        row.addEventListener('click', () => {
            // При клике переходим по URL, указанному в атрибуте 'data-href'
            window.location.href = row.dataset.href;
        });
    });
});