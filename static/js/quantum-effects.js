// Quantum Effects System
class QuantumEffects {
    constructor() {
        this.particles = [];
        this.maxParticles = 50;
        this.effectsEnabled = true;
        this.quantumState = {
            coherence: 0.85,
            entanglement: 0.75,
            particles: 100
        };
        this.init();
    }

    init() {
        // Create particle container
        this.particleContainer = document.createElement('div');
        this.particleContainer.id = 'particle-container';
        this.particleContainer.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 9995;
        `;
        document.body.appendChild(this.particleContainer);

        // Start particle system
        this.startParticleSystem();

        // Update quantum state periodically
        this.updateQuantumState();

        // Button hover effects
        this.setupButtonEffects();

        // Dynamic shadow system
        this.setupDynamicShadows();
    }

    startParticleSystem() {
        // Create initial particles
        for (let i = 0; i < this.maxParticles; i++) {
            this.createParticle();
        }

        // Update particles
        this.updateParticles();
    }

    createParticle() {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        
        // Random properties
        const size = Math.random() * 4 + 1;
        const x = Math.random() * window.innerWidth;
        const y = Math.random() * window.innerHeight;
        
        particle.style.cssText = `
            position: fixed;
            width: ${size}px;
            height: ${size}px;
            background: rgba(255, 215, 0, ${Math.random() * 0.5 + 0.1});
            border-radius: 50%;
            left: ${x}px;
            top: ${y}px;
            pointer-events: none;
            z-index: 9995;
        `;
        
        // Set animation variables
        const tx = (Math.random() - 0.5) * 200;
        const ty = (Math.random() - 0.5) * 200;
        particle.style.setProperty('--tx', `${tx}px`);
        particle.style.setProperty('--ty', `${ty}px`);
        
        // Animation duration
        const duration = Math.random() * 2 + 1;
        particle.style.animationDuration = `${duration}s`;
        
        this.particleContainer.appendChild(particle);
        
        this.particles.push({
            element: particle,
            x, y,
            vx: (Math.random() - 0.5) * 2,
            vy: (Math.random() - 0.5) * 2,
            life: duration * 1000,
            born: Date.now()
        });
    }

    updateParticles() {
        const now = Date.now();
        
        // Update existing particles
        for (let i = this.particles.length - 1; i >= 0; i--) {
            const particle = this.particles[i];
            
            // Check if particle should die
            if (now - particle.born > particle.life) {
                particle.element.remove();
                this.particles.splice(i, 1);
                this.createParticle(); // Replace with new particle
                continue;
            }
            
            // Update position
            particle.x += particle.vx;
            particle.y += particle.vy;
            
            // Bounce off walls
            if (particle.x < 0 || particle.x > window.innerWidth) particle.vx *= -1;
            if (particle.y < 0 || particle.y > window.innerHeight) particle.vy *= -1;
            
            // Apply quantum jitter
            if (Math.random() < 0.01) {
                particle.vx += (Math.random() - 0.5) * 0.5;
                particle.vy += (Math.random() - 0.5) * 0.5;
            }
            
            // Update element position
            particle.element.style.left = `${particle.x}px`;
            particle.element.style.top = `${particle.y}px`;
            
            // Update opacity based on life
            const lifeRatio = 1 - ((now - particle.born) / particle.life);
            particle.element.style.opacity = (lifeRatio * 0.3).toString();
        }
        
        // Continue animation
        requestAnimationFrame(() => this.updateParticles());
    }

    updateQuantumState() {
        // Fetch quantum state from server
        fetch('/api/quantum-state')
            .then(response => response.json())
            .then(data => {
                this.quantumState = data;
                this.updateVisualEffects();
            })
            .catch(error => {
                console.error('Error fetching quantum state:', error);
                // Fallback to simulated data
                this.quantumState.coherence = 0.7 + Math.random() * 0.25;
                this.quantumState.entanglement = 0.6 + Math.random() * 0.3;
                this.updateVisualEffects();
            });
        
        // Update every 5 seconds
        setTimeout(() => this.updateQuantumState(), 5000);
    }

    updateVisualEffects() {
        // Update particle count based on quantum state
        const targetParticles = Math.floor(this.quantumState.particles * 0.5);
        
        if (targetParticles > this.particles.length) {
            const needed = targetParticles - this.particles.length;
            for (let i = 0; i < needed; i++) {
                this.createParticle();
            }
        }
        
        // Update background noise intensity
        const noiseElement = document.getElementById('quantum-noise');
        if (noiseElement) {
            noiseElement.style.opacity = (0.3 + this.quantumState.coherence * 0.2).toString();
        }
    }

    setupButtonEffects() {
        const buttons = document.querySelectorAll('.action-button');
        
        buttons.forEach(button => {
            // Mouse enter effect
            button.addEventListener('mouseenter', (e) => {
                if (!this.effectsEnabled) return;
                
                // Add quantum hover class
                button.classList.add('quantum-hover');
                
                // Create particles around button
                this.createButtonParticles(e.target);
            });
            
            // Mouse leave effect
            button.addEventListener('mouseleave', () => {
                button.classList.remove('quantum-hover');
            });
            
            // Click effect
            button.addEventListener('click', (e) => {
                if (!this.effectsEnabled) return;
                
                // Create click explosion
                this.createClickExplosion(e.clientX, e.clientY);
                
                // Quantum tunneling effect
                if (Math.random() < 0.3) {
                    this.createQuantumTunnel(e.clientX, e.clientY);
                }
            });
        });
    }

    createButtonParticles(button) {
        const rect = button.getBoundingClientRect();
        const particleCount = 10;
        
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.classList.add('particle');
            
            const size = Math.random() * 3 + 1;
            const x = rect.left + Math.random() * rect.width;
            const y = rect.top + Math.random() * rect.height;
            
            particle.style.cssText = `
                position: fixed;
                width: ${size}px;
                height: ${size}px;
                background: rgba(255, 215, 0, ${Math.random() * 0.8 + 0.2});
                border-radius: 50%;
                left: ${x}px;
                top: ${y}px;
                pointer-events: none;
                z-index: 9996;
            `;
            
            // Animate outward
            const angle = Math.random() * Math.PI * 2;
            const distance = Math.random() * 50 + 20;
            const tx = Math.cos(angle) * distance;
            const ty = Math.sin(angle) * distance;
            
            particle.style.setProperty('--tx', `${tx}px`);
            particle.style.setProperty('--ty', `${ty}px`);
            particle.style.animationDuration = '0.8s';
            
            this.particleContainer.appendChild(particle);
            
            // Remove after animation
            setTimeout(() => {
                if (particle.parentNode) {
                    particle.remove();
                }
            }, 800);
        }
    }

    createClickExplosion(x, y) {
        const explosionCount = 15;
        
        for (let i = 0; i < explosionCount; i++) {
            const particle = document.createElement('div');
            particle.classList.add('particle');
            
            const size = Math.random() * 4 + 2;
            const angle = Math.random() * Math.PI * 2;
            const speed = Math.random() * 3 + 1;
            
            particle.style.cssText = `
                position: fixed;
                width: ${size}px;
                height: ${size}px;
                background: rgba(255, 215, 0, ${Math.random() * 0.9 + 0.1});
                border-radius: 50%;
                left: ${x}px;
                top: ${y}px;
                pointer-events: none;
                z-index: 9996;
            `;
            
            // Animate outward with physics
            const distance = speed * 50;
            const tx = Math.cos(angle) * distance;
            const ty = Math.sin(angle) * distance;
            
            particle.style.setProperty('--tx', `${tx}px`);
            particle.style.setProperty('--ty', `${ty}px`);
            particle.style.animationDuration = '0.6s';
            
            this.particleContainer.appendChild(particle);
            
            // Remove after animation
            setTimeout(() => {
                if (particle.parentNode) {
                    particle.remove();
                }
            }, 600);
        }
    }

    createQuantumTunnel(x, y) {
        const tunnel = document.createElement('div');
        tunnel.classList.add('quantum-tunnel');
        
        const size = Math.random() * 40 + 20;
        tunnel.style.cssText = `
            position: fixed;
            width: ${size}px;
            height: ${size}px;
            left: ${x - size/2}px;
            top: ${y - size/2}px;
            pointer-events: none;
            z-index: 9997;
            background: radial-gradient(circle, 
                rgba(255, 215, 0, 0.6) 0%, 
                rgba(255, 215, 0, 0.3) 30%,
                transparent 70%);
            border-radius: 50%;
            animation: tunnel-pop 0.4s ease-out forwards;
        `;
        
        document.body.appendChild(tunnel);
        
        // Remove after animation
        setTimeout(() => {
            if (tunnel.parentNode) {
                tunnel.remove();
            }
        }, 400);
    }

    setupDynamicShadows() {
        // Update shadows based on cursor position
        document.addEventListener('mousemove', (e) => {
            if (!this.effectsEnabled) return;
            
            const x = e.clientX / window.innerWidth;
            const y = e.clientY / window.innerHeight;
            
            // Calculate shadow offsets based on cursor position
            const offsetX = (x - 0.5) * 20;
            const offsetY = (y - 0.5) * 20;
            
            // Update elements with dynamic shadows
            const elements = document.querySelectorAll('.dynamic-shadow');
            elements.forEach(element => {
                element.style.boxShadow = `
                    ${offsetX}px ${offsetY}px 30px rgba(0, 0, 0, 0.5),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1)
                `;
            });
        });
    }

    toggleEffects() {
        this.effectsEnabled = !this.effectsEnabled;
        
        if (this.effectsEnabled) {
            this.particleContainer.style.display = 'block';
        } else {
            this.particleContainer.style.display = 'none';
        }
        
        return this.effectsEnabled;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.quantumEffects = new QuantumEffects();
});