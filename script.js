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
        let currentIndex = 1; // Start from the first actual slide (after the clone)
        let isTransitioning = false;

        // Clone first and last slides for infinite loop
        const firstClone = slides[0].cloneNode(true);
        const lastClone = slides[slides.length - 1].cloneNode(true);
        reviewsContainer.appendChild(firstClone);
        reviewsContainer.insertBefore(lastClone, slides[0]);

        // Update slides array with clones
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

        const handleNext = () => {
            if (isTransitioning) return;
            currentIndex++;
            shiftSlides();
        };

        const handlePrev = () => {
            if (isTransitioning) return;
            currentIndex--;
            shiftSlides();
        };

        nextButton.addEventListener('click', handleNext);
        prevButton.addEventListener('click', handlePrev);

        window.addEventListener('resize', () => {
            reviewsContainer.style.transition = 'none';
            setPosition();
        });

        // Initial position without transition
        reviewsContainer.style.transition = 'none';
        setPosition();
    }
});
