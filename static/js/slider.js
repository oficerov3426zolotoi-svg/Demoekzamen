document.addEventListener('DOMContentLoaded', function() {
    const slider = document.querySelector('.slider-wrapper');
    const dots = document.querySelectorAll('.slider-dot');
    const prevBtn = document.querySelector('.slider-controls.prev');
    const nextBtn = document.querySelector('.slider-controls.next');
    
    if (!slider) return;
    
    let currentSlide = 0;
    const slideCount = dots.length;
    let autoSlideInterval;
    
    function goToSlide(index) {
        currentSlide = index;
        slider.style.transform = `translateX(-${currentSlide * 100}%)`;
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === currentSlide);
        });
    }
    
    function nextSlide() {
        goToSlide((currentSlide + 1) % slideCount);
    }
    
    function prevSlide() {
        goToSlide((currentSlide - 1 + slideCount) % slideCount);
    }
    
    function startAutoSlide() {
        autoSlideInterval = setInterval(nextSlide, 3000);
    }
    
    function stopAutoSlide() {
        clearInterval(autoSlideInterval);
    }
    
    if (nextBtn) nextBtn.addEventListener('click', () => {
        stopAutoSlide();
        nextSlide();
        startAutoSlide();
    });
    
    if (prevBtn) prevBtn.addEventListener('click', () => {
        stopAutoSlide();
        prevSlide();
        startAutoSlide();
    });
    
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            stopAutoSlide();
            goToSlide(index);
            startAutoSlide();
        });
    });
    
    startAutoSlide();
});