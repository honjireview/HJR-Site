document.addEventListener('DOMContentLoaded', function() {
    // --- Logic for Main Page (index.html) ---
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuButton) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // --- Logic for Bot Page (bot.html) ---
    const mobileMenuButtonBot = document.getElementById('mobile-menu-button-bot');
    const mobileMenuBot = document.getElementById('mobile-menu-bot');

    if (mobileMenuButtonBot) {
        mobileMenuButtonBot.addEventListener('click', () => {
            mobileMenuBot.classList.toggle('hidden');
        });
    }

    const problemTabs = document.querySelectorAll('.problem-tab');
    const solutionContents = document.querySelectorAll('.solution-content');

    problemTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetId = tab.dataset.tab;

            problemTabs.forEach(t => {
                t.classList.remove('tab-active');
                t.classList.add('tab-inactive');
            });
            tab.classList.remove('tab-inactive');
            tab.classList.add('tab-active');

            solutionContents.forEach(content => {
                if (content.id === targetId) {
                    content.classList.remove('hidden');
                } else {
                    content.classList.add('hidden');
                }
            });
        });
    });

    const faqQuestions = document.querySelectorAll('.faq-question');
    faqQuestions.forEach(question => {
        question.addEventListener('click', () => {
            const answer = question.nextElementSibling;
            const arrow = question.querySelector('.arrow-down');

            const isOpening = !answer.style.maxHeight || answer.style.maxHeight === '0px';

            // Close all other answers
            faqQuestions.forEach(q => {
                const ans = q.nextElementSibling;
                if (ans !== answer) {
                    ans.style.maxHeight = '0px';
                    q.querySelector('.arrow-down').classList.remove('rotated');
                }
            });

            // Toggle the clicked one
            if (isOpening) {
                answer.style.maxHeight = answer.scrollHeight + 'px';
                arrow.classList.add('rotated');
            } else {
                answer.style.maxHeight = '0px';
                arrow.classList.remove('rotated');
            }
        });
    });
});
