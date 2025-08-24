// This script contains all the interactive logic for the bot showcase page.
document.addEventListener('DOMContentLoaded', function() {

    // --- Splash Screen Logic ---
    const body = document.body;
    const splashScreen = document.getElementById('splash-screen');

    if (splashScreen) {
        body.classList.add('no-scroll'); // Prevent scrolling while splash is visible

        // Trigger the "zoom in" animation shortly after the page loads
        setTimeout(() => {
            splashScreen.classList.add('visible');
        }, 50);

        // Start the "zoom out" animation after a delay
        setTimeout(() => {
            splashScreen.classList.remove('visible');

            // Remove the element from the DOM after the exit animation completes
            setTimeout(() => {
                if (splashScreen) {
                    splashScreen.remove();
                }
                body.classList.remove('no-scroll'); // Allow scrolling again
            }, 500); // This MUST match the CSS transition duration

        }, 3050); // Total time visible
    }

    // --- Mobile Menu Logic ---
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // --- Tabs Logic for "Problems and Solutions" section ---
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

    // --- Accordion Logic for FAQ section ---
    const faqQuestions = document.querySelectorAll('.faq-question');
    if (faqQuestions.length > 0) {
        faqQuestions.forEach(question => {
            question.addEventListener('click', () => {
                const answer = question.nextElementSibling;
                const arrow = question.querySelector('.arrow-down');
                const isOpening = !answer.style.maxHeight || answer.style.maxHeight === '0px';

                // Close all other open FAQs
                faqQuestions.forEach(q => {
                    if (q !== question) {
                        q.nextElementSibling.style.maxHeight = '0px';
                        if (q.querySelector('.arrow-down')) {
                            q.querySelector('.arrow-down').classList.remove('rotated');
                        }
                    }
                });

                // Open or close the clicked FAQ
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

    // --- Scroll-to-Top Button Logic ---
    const scrollToTopButton = document.getElementById('scroll-to-top');
    if (scrollToTopButton) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                scrollToTopButton.classList.remove('hidden');
            } else {
                scrollToTopButton.classList.add('hidden');
            }
        });

        scrollToTopButton.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // --- Animate sections on scroll (Intersection Observer) ---
    const sectionsToAnimate = document.querySelectorAll('.fade-in-section, .animated-children-container');
    if (sectionsToAnimate.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1 // Trigger when 10% of the element is visible
        });

        sectionsToAnimate.forEach(section => {
            observer.observe(section);
        });
    }

    // --- Active Nav Link Highlighting on Scroll ---
    const navLinks = document.querySelectorAll('.nav-link');
    const pageSections = document.querySelectorAll('main section');
    if (navLinks.length > 0 && pageSections.length > 0) {
        const highlightNavLink = () => {
            let currentSectionId = '';
            pageSections.forEach(section => {
                const sectionTop = section.offsetTop;
                if (scrollY >= sectionTop - 100) { // 100px offset
                    currentSectionId = section.getAttribute('id');
                }
            });

            if (window.scrollY < 300) {
                currentSectionId = 'hero';
            }

            navLinks.forEach(link => {
                link.classList.remove('nav-link-active');
                if (link.getAttribute('href') === `#${currentSectionId}`) {
                    link.classList.add('nav-link-active');
                }
            });
        };

        window.addEventListener('scroll', highlightNavLink);
        highlightNavLink(); // Initial call
    }
});