document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu logic
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuButton) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Reviews slider logic
    const reviewsContainer = document.getElementById('reviews-container');
    const prevButton = document.getElementById('prev-slide');
    const nextButton = document.getElementById('next-slide');

    if (reviewsContainer && prevButton && nextButton) {
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
            if (currentIndex === 0) {
                reviewsContainer.style.transition = 'none';
                currentIndex = slides.length - 2;
                setPosition();
            }
            if (currentIndex === slides.length - 1) {
                reviewsContainer.style.transition = 'none';
                currentIndex = 1;
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
});
