document.addEventListener('DOMContentLoaded', function() {

    // --- Mobile Menu Logic ---
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenuButton) {
        mobileMenuButton.addEventListener('click', () => mobileMenu.classList.toggle('hidden'));
    }

    const mobileMenuButtonBot = document.getElementById('mobile-menu-button-bot');
    const mobileMenuBot = document.getElementById('mobile-menu-bot');
    if (mobileMenuButtonBot) {
        mobileMenuButtonBot.addEventListener('click', () => mobileMenuBot.classList.toggle('hidden'));
    }

    // --- Reviews Slider Logic (for index.html) ---
    const reviewsContainer = document.getElementById('reviews-container');
    if (reviewsContainer) {
        const prevButton = document.getElementById('prev-slide');
        const nextButton = document.getElementById('next-slide');
        let slides = Array.from(reviewsContainer.children);
        let currentIndex = 1;
        let isTransitioning = false;

        const firstClone = slides[0].cloneNode(true);
        const lastClone = slides[slides.length - 1].cloneNode(true);
        reviewsContainer.appendChild(firstClone);
        reviewsContainer.insertBefore(lastClone, slides[0]);
        slides = Array.from(reviewsContainer.children);

        const slideWidth = () => slides[0].getBoundingClientRect().width;
        const setPosition = () => {
            reviewsContainer.style.transform = `translateX(-${currentIndex * slideWidth()}px)`;
        };
        const shiftSlides = () => {
            isTransitioning = true;
            reviewsContainer.style.transition = 'transform 0.5s ease-in-out';
            setPosition();
        };

        reviewsContainer.addEventListener('transitionend', () => {
            isTransitioning = false;
            if (currentIndex === 0 || currentIndex === slides.length - 1) {
                reviewsContainer.style.transition = 'none';
                currentIndex = (currentIndex === 0) ? slides.length - 2 : 1;
                setPosition();
            }
        });

        nextButton.addEventListener('click', () => {
            if (isTransitioning) return;
            currentIndex++;
            shiftSlides();
        });
        prevButton.addEventListener('click', () => {
            if (isTransitioning) return;
            currentIndex--;
            shiftSlides();
        });
        window.addEventListener('resize', () => {
            reviewsContainer.style.transition = 'none';
            setPosition();
        });
        reviewsContainer.style.transition = 'none';
        setPosition();
    }

    // --- Tabs & Accordion Logic (for bot.html) ---
    const problemTabs = document.querySelectorAll('.problem-tab');
    if (problemTabs.length > 0) {
        const solutionContents = document.querySelectorAll('.solution-content');
        problemTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const targetId = tab.dataset.tab;
                problemTabs.forEach(t => {
                    t.classList.remove('tab-active');
                    t.classList.add('tab-inactive');
                });
                tab.classList.replace('tab-inactive', 'tab-active');
                solutionContents.forEach(c => c.id === targetId ? c.classList.remove('hidden') : c.classList.add('hidden'));
            });
        });
    }

    const faqQuestions = document.querySelectorAll('.faq-question');
    if (faqQuestions.length > 0) {
        faqQuestions.forEach(question => {
            question.addEventListener('click', () => {
                const answer = question.nextElementSibling;
                const arrow = question.querySelector('.arrow-down');
                const isOpening = !answer.style.maxHeight || answer.style.maxHeight === '0px';

                faqQuestions.forEach(q => {
                    if (q !== question) {
                        q.nextElementSibling.style.maxHeight = '0px';
                        if (q.querySelector('.arrow-down')) q.querySelector('.arrow-down').classList.remove('rotated');
                    }
                });

                if (isOpening) {
                    answer.style.maxHeight = answer.scrollHeight + 'px';
                    if (arrow) arrow.classList.add('rotated');
                } else {
                    answer.style.maxHeight = '0px';
                    if (arrow) arrow.classList.remove('rotated');
                }
            });
        });
    }
});
