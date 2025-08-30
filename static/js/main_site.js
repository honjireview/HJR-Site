// static/js/main_site.js
document.addEventListener('DOMContentLoaded', () => {
    // --- Language Switcher Logic ---
    const langButton = document.getElementById('lang-switcher-button');
    const langMenu = document.getElementById('lang-switcher-menu');

    if (langButton && langMenu) {
        langButton.addEventListener('click', (event) => {
            event.stopPropagation(); // Prevent the click from immediately closing the menu
            langMenu.style.display = langMenu.style.display === 'block' ? 'none' : 'block';
        });

        // Close the dropdown if clicking outside of it
        document.addEventListener('click', (event) => {
            if (!langButton.contains(event.target) && !langMenu.contains(event.target)) {
                langMenu.style.display = 'none';
            }
        });
    }
});