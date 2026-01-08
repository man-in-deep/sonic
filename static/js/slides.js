// Slide Carousel System
class SlideCarousel {
    constructor() {
        this.slides = [];
        this.currentSlide = 0;
        this.totalSlides = 0;
        this.autoRotate = true;
        this.rotateInterval = 8000; // 8 seconds
        this.intervalId = null;
        this.init();
    }

    init() {
        // Get all slides
        this.slides = Array.from(document.querySelectorAll('.slide'));
        this.totalSlides = this.slides.length;
        
        // Get navigation dots
        this.createNavigationDots();
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Show first slide
        this.showSlide(0);
        
        // Start auto rotation
        this.startAutoRotation();
    }

    createNavigationDots() {
        const dotsContainer = document.querySelector('.navigation-dots');
        
        // Clear existing dots
        dotsContainer.innerHTML = '';
        
        // Create dots
        for (let i = 0; i < this.totalSlides; i++) {
            const dot = document.createElement('div');
            dot.classList.add('dot');
            dot.dataset.index = i;
            
            // Add quantum state indicator
            const quantumState = document.createElement('div');
            quantumState.classList.add('quantum-state');
            quantumState.style.width = '100%';
            quantumState.style.height = '100%';
            quantumState.style.borderRadius = '50%';
            quantumState.style.background = 'radial-gradient(circle, rgba(255,215,0,0.3) 0%, transparent 70%)';
            quantumState.style.animation = `quantum-pulse ${2 + i * 0.5}s ease-in-out infinite`;
            
            dot.appendChild(quantumState);
            dotsContainer.appendChild(dot);
            
            // Click event
            dot.addEventListener('click', () => {
                this.showSlide(i);
                this.resetAutoRotation();
            });
        }
    }

    setupEventListeners() {
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') {
                this.prevSlide();
            } else if (e.key === 'ArrowRight') {
                this.nextSlide();
            } else if (e.key === ' ') {
                this.toggleAutoRotation();
            }
        });

        // Touch/swipe support
        let touchStartX = 0;
        let touchEndX = 0;

        document.querySelector('.slide-container').addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
        });

        document.querySelector('.slide-container').addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            this.handleSwipe(touchStartX, touchEndX);
        });

        // Pause auto-rotation on hover
        const slideContainer = document.querySelector('.slide-container');
        slideContainer.addEventListener('mouseenter', () => {
            this.pauseAutoRotation();
        });

        slideContainer.addEventListener('mouseleave', () => {
            if (this.autoRotate) {
                this.startAutoRotation();
            }
        });
    }

    showSlide(index) {
        // Validate index
        if (index < 0) index = this.totalSlides - 1;
        if (index >= this.totalSlides) index = 0;
        
        // Update current slide
        this.currentSlide = index;
        
        // Hide all slides
        this.slides.forEach(slide => {
            slide.classList.remove('active');
            slide.classList.remove('slide-enter');
            slide.classList.remove('slide-exit');
        });
        
        // Show current slide with animation
        const currentSlide = this.slides[this.currentSlide];
        currentSlide.classList.add('active');
        currentSlide.classList.add('slide-enter');
        
        // Update navigation dots
        this.updateNavigationDots();
        
        // Update quantum state indicator
        this.updateQuantumIndicator();
    }

    updateNavigationDots() {
        const dots = document.querySelectorAll('.dot');
        dots.forEach((dot, index) => {
            if (index === this.currentSlide) {
                dot.classList.add('active');
            } else {
                dot.classList.remove('active');
            }
        });
    }

    updateQuantumIndicator() {
        // Calculate quantum coherence based on slide position
        const coherence = 0.7 + (this.currentSlide / this.totalSlides) * 0.25;
        const fillElement = document.querySelector('.indicator-fill');
        const valueElement = document.querySelector('.indicator-value');
        
        if (fillElement && valueElement) {
            fillElement.style.width = `${coherence * 100}%`;
            valueElement.textContent = `${Math.round(coherence * 100)}%`;
        }
    }

    nextSlide() {
        this.showSlide(this.currentSlide + 1);
        this.resetAutoRotation();
    }

    prevSlide() {
        this.showSlide(this.currentSlide - 1);
        this.resetAutoRotation();
    }

    handleSwipe(startX, endX) {
        const threshold = 50;
        const diff = startX - endX;
        
        if (Math.abs(diff) > threshold) {
            if (diff > 0) {
                this.nextSlide();
            } else {
                this.prevSlide();
            }
        }
    }

    startAutoRotation() {
        if (this.autoRotate && !this.intervalId) {
            this.intervalId = setInterval(() => {
                this.nextSlide();
            }, this.rotateInterval);
        }
    }

    pauseAutoRotation() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }

    resetAutoRotation() {
        this.pauseAutoRotation();
        if (this.autoRotate) {
            this.startAutoRotation();
        }
    }

    toggleAutoRotation() {
        this.autoRotate = !this.autoRotate;
        if (this.autoRotate) {
            this.startAutoRotation();
        } else {
            this.pauseAutoRotation();
        }
        
        // Visual feedback
        const indicator = document.querySelector('.quantum-indicator');
        if (indicator) {
            indicator.style.animation = 'quantum-appear 0.5s ease-out';
            setTimeout(() => {
                indicator.style.animation = '';
            }, 500);
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.slideCarousel = new SlideCarousel();
});