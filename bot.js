document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu logic for bot page
    const mobileMenuButtonBot = document.getElementById('mobile-menu-button-bot');
    const mobileMenuBot = document.getElementById('mobile-menu-bot');

    if (mobileMenuButtonBot) {
        mobileMenuButtonBot.addEventListener('click', () => {
            mobileMenuBot.classList.toggle('hidden');
        });
    }

    // Tabs logic for problems section
    const problemTabs = document.querySelectorAll('.problem-tab');
    const solutionContents = document.querySelectorAll('.solution-content');

    if (problemTabs.length > 0) {
        problemTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const targetId = tab.dataset.tab;
                problemTabs.forEach(t => {
                    t.classList.remove('tab-active');
                    t.classList.add('tab-inactive');
                });
                tab.classList.remove('tab-inactive');
                tab.classList.add('tab-active');
                solutionContents.forEach(c => c.id === targetId ? c.classList.remove('hidden') : c.classList.add('hidden'));
            });
        });
    }

    // Accordion logic for FAQ section
    const faqQuestions = document.querySelectorAll('.faq-question');
    if (faqQuestions.length > 0) {
        faqQuestions.forEach(question => {
            question.addEventListener('click', () => {
                const answer = question.nextElementSibling;
                const arrow = question.querySelector('.arrow-down');
                const isOpening = !answer.style.maxHeight || answer.style.maxHeight === '0px';

                faqQuestions.forEach(q => {
                    if(q !== question) {
                        q.nextElementSibling.style.maxHeight = '0px';
                        if(q.querySelector('.arrow-down')) q.querySelector('.arrow-down').classList.remove('rotated');
                    }
                });

                if (isOpening) {
                    answer.style.maxHeight = answer.scrollHeight + 'px';
                    if(arrow) arrow.classList.add('rotated');
                } else {
                    answer.style.maxHeight = '0px';
                    if(arrow) arrow.classList.remove('rotated');
                }
            });
        });
    }
});
