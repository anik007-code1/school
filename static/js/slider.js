document.addEventListener('DOMContentLoaded', function() {
    const sliderContainer = document.querySelector('.slider-container');
    if (!sliderContainer) return;

    const slides = Array.from(document.querySelectorAll('.slide'));
    const dots = Array.from(document.querySelectorAll('.slider-dot'));
    const prevBtn = document.querySelector('.slider-prev');
    const nextBtn = document.querySelector('.slider-next');
    let currentSlide = 0;
    let interval = null;

    // Function to show a specific slide
    function showSlide(index) {
        // Hide all slides first
        slides.forEach(slide => {
            slide.style.opacity = '0';
            slide.style.zIndex = '0';
        });
        dots.forEach(dot => dot.classList.remove('bg-opacity-100'));
        
        // Show the target slide
        if (slides[index]) {
            slides[index].style.opacity = '1';
            slides[index].style.zIndex = '1';
        }
        if (dots[index]) {
            dots[index].classList.add('bg-opacity-100');
        }
        currentSlide = index;
    }

    // Function to show next slide
    function nextSlide() {
        const next = (currentSlide + 1) % slides.length;
        showSlide(next);
    }

    // Function to show previous slide
    function prevSlide() {
        const prev = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(prev);
    }

    // Event listeners for navigation buttons
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            prevSlide();
            resetInterval();
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            nextSlide();
            resetInterval();
        });
    }

    // Event listeners for dots
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            showSlide(index);
            resetInterval();
        });
    });

    // Auto-advance slides
    function startInterval() {
        interval = setInterval(nextSlide, 5000); // Change slide every 5 seconds
    }

    function resetInterval() {
        if (interval) {
            clearInterval(interval);
            startInterval();
        }
    }

    // Start auto-advance if there's more than one slide
    if (slides.length > 1) {
        startInterval();
    }
});
