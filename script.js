document.addEventListener('DOMContentLoaded', function() {
    // --- Logic for Main Page (index.html) ---
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuButton) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // --- Reviews Slider Logic ---
    const reviewsContainer = document.getElementById('reviews-container');
    const prevButton = document.getElementById('prev-slide');
    const nextButton = document.getElementById('next-slide');

    if (reviewsContainer && prevButton && nextButton) {
        let slides = Array.from(reviewsContainer.children);
        let currentIndex = 0;
        let slideWidth = 0;

        // Clone slides for infinite loop effect
        const clones = slides.map(slide => slide.cloneNode(true));
        reviewsContainer.append(...clones);
        slides = Array.from(reviewsContainer.children);

        function updateSlideWidth() {
            slideWidth = slides[0].getBoundingClientRect().width;
        }

        function goToSlide(index, smooth = true) {
            if (!smooth) {
                reviewsContainer.style.transition = 'none';
            }
            reviewsContainer.style.transform = `translateX(-${index * slideWidth}px)`;
            if (!smooth) {
                // Force reflow
                reviewsContainer.offsetHeight;
                reviewsContainer.style.transition = 'transform 0.5s ease-in-out';
            }
        }

        function handleNext() {
            currentIndex++;
            goToSlide(currentIndex);

            if (currentIndex >= slides.length / 2) {
                setTimeout(() => {
                    currentIndex = 0;
                    goToSlide(currentIndex, false);
                }, 500); // Match transition duration
            }
        }

        function handlePrev() {
            if (currentIndex === 0) {
                currentIndex = slides.length / 2;
                goToSlide(currentIndex, false);
            }

            setTimeout(() => {
                currentIndex--;
                goToSlide(currentIndex);
            }, 10);
        }

        nextButton.addEventListener('click', handleNext);
        prevButton.addEventListener('click', handlePrev);

        window.addEventListener('resize', () => {
            updateSlideWidth();
            goToSlide(currentIndex, false);
        });

        // Initial setup
        updateSlideWidth();
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

            faqQuestions.forEach(q => {
                const ans = q.nextElementSibling;
                if (ans !== answer) {
                    ans.style.maxHeight = '0px';
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
});
