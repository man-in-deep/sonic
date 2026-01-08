// Pencil Cursor System
class PencilCursor {
    constructor() {
        this.cursor = null;
        this.trails = [];
        this.maxTrails = 100;
        this.trailLife = 500; // ms
        this.isEraser = false;
        this.lastPosition = { x: 0, y: 0 };
        this.speed = 0;
        this.lastTime = Date.now();
        this.quantumTunnelingProbability = 0.01;
        this.init();
    }

    init() {
        // Create custom cursor
        this.cursor = document.createElement('div');
        this.cursor.id = 'custom-cursor';
        this.cursor.classList.add('pencil');
        document.body.appendChild(this.cursor);

        // Create quantum noise field
        this.createQuantumNoise();

        // Event listeners
        document.addEventListener('mousemove', (e) => this.onMouseMove(e));
        document.addEventListener('mousedown', (e) => this.onMouseDown(e));
        document.addEventListener('mouseup', (e) => this.onMouseUp(e));
        document.addEventListener('contextmenu', (e) => this.onRightClick(e));

        // Update cursor position
        this.updatePosition = this.updatePosition.bind(this);
        requestAnimationFrame(this.updatePosition);

        // Clean up old trails
        setInterval(() => this.cleanupTrails(), 1000);
    }

    createQuantumNoise() {
        const noise = document.createElement('div');
        noise.id = 'quantum-noise';
        document.body.appendChild(noise);
    }

    onMouseMove(e) {
        this.lastPosition = { x: e.clientX, y: e.clientY };
        
        // Calculate speed
        const currentTime = Date.now();
        const deltaTime = currentTime - this.lastTime;
        const dx = e.clientX - this.lastPosition.x;
        const dy = e.clientY - this.lastPosition.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        this.speed = distance / deltaTime;
        this.lastTime = currentTime;

        // Create pencil trail
        this.createTrail(e.clientX, e.clientY);

        // Quantum tunneling effect
        if (Math.random() < this.quantumTunnelingProbability) {
            this.createQuantumTunnel(e.clientX + (Math.random() * 100 - 50), 
                                   e.clientY + (Math.random() * 100 - 50));
        }
    }

    createTrail(x, y) {
        // Calculate opacity based on speed (slower = darker)
        const opacity = Math.max(0.1, Math.min(0.9, 1 - this.speed * 10));
        
        // Calculate size based on speed (slower = thicker)
        const size = Math.max(2, Math.min(8, 10 - this.speed * 50));
        
        // Create trail element
        const trail = document.createElement('div');
        trail.classList.add('pencil-trail');
        
        // Apply styles
        trail.style.width = `${size}px`;
        trail.style.height = `${size}px`;
        trail.style.left = `${x - size/2}px`;
        trail.style.top = `${y - size/2}px`;
        trail.style.opacity = opacity.toString();
        trail.style.background = this.isEraser ? 
            'radial-gradient(circle, rgba(255,255,255,0.8) 0%, transparent 70%)' :
            'radial-gradient(circle, rgba(255,215,0,0.8) 0%, transparent 70%)';
        
        // Add paper grain effect
        trail.style.backgroundImage = `
            radial-gradient(circle at 30% 30%, rgba(0,0,0,0.1) 1px, transparent 1px),
            radial-gradient(circle at 70% 70%, rgba(0,0,0,0.1) 1px, transparent 1px)
        `;
        trail.style.backgroundSize = '20px 20px';
        
        // Add quantum decay timing
        const decayTime = 500 + (Math.random() * 200 - 100); // 500ms ± 100ms
        trail.style.animationDuration = `${decayTime}ms`;
        
        document.body.appendChild(trail);
        
        // Store trail reference
        this.trails.push({
            element: trail,
            timestamp: Date.now()
        });

        // Limit number of trails
        if (this.trails.length > this.maxTrails) {
            const oldest = this.trails.shift();
            if (oldest.element.parentNode) {
                oldest.element.remove();
            }
        }
    }

    createQuantumTunnel(x, y) {
        const tunnel = document.createElement('div');
        tunnel.classList.add('quantum-tunnel');
        
        tunnel.style.width = '50px';
        tunnel.style.height = '50px';
        tunnel.style.left = `${x - 25}px`;
        tunnel.style.top = `${y - 25}px`;
        
        document.body.appendChild(tunnel);
        
        // Remove after animation
        setTimeout(() => {
            if (tunnel.parentNode) {
                tunnel.remove();
            }
        }, 300);
    }

    cleanupTrails() {
        const now = Date.now();
        const cutoff = now - this.trailLife;
        
        while (this.trails.length > 0 && this.trails[0].timestamp < cutoff) {
            const trail = this.trails.shift();
            if (trail.element.parentNode) {
                trail.element.remove();
            }
        }
    }

    onMouseDown(e) {
        if (e.button === 2) { // Right click
            this.isEraser = true;
            this.cursor.classList.remove('pencil');
            this.cursor.classList.add('eraser');
        }
    }

    onMouseUp(e) {
        if (e.button === 2) { // Right click
            this.isEraser = false;
            this.cursor.classList.remove('eraser');
            this.cursor.classList.add('pencil');
        }
    }

    onRightClick(e) {
        e.preventDefault();
        return false;
    }

    updatePosition() {
        if (this.cursor && this.lastPosition) {
            // Smooth cursor movement
            const currentX = parseFloat(this.cursor.style.left) || this.lastPosition.x;
            const currentY = parseFloat(this.cursor.style.top) || this.lastPosition.y;
            
            const targetX = this.lastPosition.x;
            const targetY = this.lastPosition.y;
            
            const newX = currentX + (targetX - currentX) * 0.3;
            const newY = currentY + (targetY - currentY) * 0.3;
            
            this.cursor.style.left = `${newX - 16}px`;
            this.cursor.style.top = `${newY - 16}px`;
            
            // Add slight rotation based on movement direction
            if (Math.abs(targetX - currentX) > 1 || Math.abs(targetY - currentY) > 1) {
                const angle = Math.atan2(targetY - currentY, targetX - currentX) * (180 / Math.PI);
                this.cursor.style.transform = `rotate(${angle}deg)`;
            }
        }
        
        requestAnimationFrame(this.updatePosition);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.pencilCursor = new PencilCursor();
});