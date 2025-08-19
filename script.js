document.addEventListener('DOMContentLoaded', function() {

    // --- Mobile Menu Logic ---
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenuButton) {
        mobileMenuButton.addEventListener('click', () => mobileMenu.classList.toggle('hidden'));
    }

    // --- Tabs & Accordion Logic ---
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
    const sections = document.querySelectorAll('.fade-in-section');
    if (sections.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target); // Optional: stop observing once it's visible
                }
            });
        }, {
            threshold: 0.1 // Trigger when 10% of the element is visible
        });

        sections.forEach(section => {
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
                if (scrollY >= sectionTop - 100) { // 100px offset for better timing
                    currentSectionId = section.getAttribute('id');
                }
            });

            navLinks.forEach(link => {
                link.classList.remove('nav-link-active');
                if (link.getAttribute('href') === `#${currentSectionId}`) {
                    link.classList.add('nav-link-active');
                }
            });
        };

        window.addEventListener('scroll', highlightNavLink);
        highlightNavLink(); // Initial call to set active link on page load
    }
});
