/**
 * Artist Module JavaScript
 * Handles art generation, canvas rendering, and quantum effects
 */

class ArtistModule {
    constructor() {
        this.canvas = null;
        this.ctx = null;
        this.strokeCanvas = null;
        this.strokeCtx = null;
        this.currentImage = null;
        this.currentStrokes = [];
        this.quantumParticles = [];
        this.isGenerating = false;
        this.generationProgress = 0;
        this.init();
    }

    init() {
        // Initialize canvases
        this.canvas = document.getElementById('drawingCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.strokeCanvas = document.getElementById('strokeCanvas');
        this.strokeCtx = this.strokeCanvas.getContext('2d');
        
        // Set canvas dimensions
        this.resizeCanvases();
        window.addEventListener('resize', () => this.resizeCanvases());
        
        // Initialize event listeners
        this.initEventListeners();
        
        // Initialize quantum particles
        this.initQuantumParticles();
        
        // Load history
        this.loadHistory();
        
        console.log('Artist Module initialized');
    }

    resizeCanvases() {
        const container = this.canvas.parentElement;
        this.canvas.width = container.clientWidth;
        this.canvas.height = container.clientHeight;
        this.strokeCanvas.width = container.clientWidth;
        this.strokeCanvas.height = container.clientHeight;
        
        // Redraw if we have an image
        if (this.currentImage) {
            this.drawImage(this.currentImage);
        }
    }

    initEventListeners() {
        // Upload area
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('referenceImage');
        
        uploadArea.addEventListener('click', () => fileInput.click());
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = '#FFD700';
            uploadArea.style.background = 'rgba(255, 215, 0, 0.1)';
        });
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.style.borderColor = 'rgba(255, 215, 0, 0.5)';
            uploadArea.style.background = 'rgba(0, 0, 0, 0.4)';
        });
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = 'rgba(255, 215, 0, 0.5)';
            uploadArea.style.background = 'rgba(0, 0, 0, 0.4)';
            
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                this.handleImageUpload(e.dataTransfer.files[0]);
            }
        });
        
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length) {
                this.handleImageUpload(e.target.files[0]);
            }
        });
        
        // Generate button
        document.getElementById('generateBtn').addEventListener('click', () => {
            this.generateArt();
        });
        
        // Clear button
        document.getElementById('clearBtn').addEventListener('click', () => {
            this.clearAll();
        });
        
        // Download button
        document.getElementById('downloadBtn').addEventListener('click', () => {
            this.downloadArt();
        });
    }

    handleImageUpload(file) {
        const preview = document.getElementById('imagePreview');
        const reader = new FileReader();
        
        reader.onload = (e) => {
            preview.src = e.target.result;
            preview.style.display = 'block';
            
            // Update upload text
            document.querySelector('.upload-text').textContent = 'Reference image loaded';
            document.querySelector('.upload-hint').textContent = 'Click to change';
        };
        
        reader.readAsDataURL(file);
    }

    async generateArt() {
        if (this.isGenerating) return;
        
        const prompt = document.getElementById('prompt').value.trim();
        const artType = document.getElementById('artType').value;
        const mediumStyle = document.getElementById('mediumStyle').value;
        
        if (!prompt) {
            this.showMessage('Please enter a description for your artwork', 'error');
            return;
        }
        
        // Show progress
        this.isGenerating = true;
        this.showProgress(true);
        this.updateProgress(10);
        this.showMessage('Initializing quantum creativity...', 'info');
        
        try {
            // Prepare form data
            const formData = new FormData();
            formData.append('prompt', prompt);
            formData.append('art_type', artType);
            formData.append('medium_style', mediumStyle);
            
            // Add reference image if exists
            const fileInput = document.getElementById('referenceImage');
            if (fileInput.files.length) {
                formData.append('reference_image', fileInput.files[0]);
            }
            
            // Update progress
            this.updateProgress(30);
            this.showMessage('Connecting to quantum AI models...', 'info');
            
            // Send request
            const response = await fetch('/api/artist/generate', {
                method: 'POST',
                body: formData
            });
            
            this.updateProgress(60);
            this.showMessage('Generating stroke-by-stroke simulation...', 'info');
            
            const result = await response.json();
            
            if (result.success) {
                this.updateProgress(90);
                this.showMessage('Applying quantum stroke effects...', 'info');
                
                // Display generated image
                this.displayGeneratedImage(result.image_data);
                
                // Display stroke simulation if available
                if (result.stroke_data) {
                    this.simulateStrokeRendering(result.stroke_data, result.stroke_count);
                }
                
                // Update quantum state
                this.updateQuantumState(result);
                
                this.updateProgress(100);
                this.showMessage('Artwork generated successfully!', 'success');
                
                // Enable download
                document.getElementById('downloadBtn').disabled = false;
                
                // Load updated history
                this.loadHistory();
            } else {
                throw new Error(result.error || 'Generation failed');
            }
            
        } catch (error) {
            this.showMessage(`Error: ${error.message}`, 'error');
            console.error('Generation error:', error);
        } finally {
            this.isGenerating = false;
            this.showProgress(false);
            this.updateProgress(0);
        }
    }

    displayGeneratedImage(imageData) {
        // Clear canvases
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.strokeCtx.clearRect(0, 0, this.strokeCanvas.width, this.strokeCanvas.height);
        
        // Create image from base64
        const img = new Image();
        img.onload = () => {
            this.currentImage = img;
            
            // Draw image centered on canvas
            const scale = Math.min(
                this.canvas.width / img.width,
                this.canvas.height / img.height
            );
            
            const width = img.width * scale;
            const height = img.height * scale;
            const x = (this.canvas.width - width) / 2;
            const y = (this.canvas.height - height) / 2;
            
            this.ctx.drawImage(img, x, y, width, height);
            
            // Add quantum particle effects
            this.createQuantumParticles(x, y, width, height);
        };
        
        img.src = `data:image/png;base64,${imageData}`;
    }

    simulateStrokeRendering(strokeData, strokeCount) {
        if (!strokeData) return;
        
        const img = new Image();
        img.onload = () => {
            // Draw stroke simulation with animation
            const scale = Math.min(
                this.strokeCanvas.width / img.width,
                this.strokeCanvas.height / img.height
            );
            
            const width = img.width * scale;
            const height = img.height * scale;
            const x = (this.strokeCanvas.width - width) / 2;
            const y = (this.strokeCanvas.height - height) / 2;
            
            // Animate stroke drawing
            this.animateStrokeDrawing(img, x, y, width, height, strokeCount);
        };
        
        img.src = `data:image/png;base64,${strokeData}`;
    }

    animateStrokeDrawing(image, x, y, width, height, strokeCount) {
        const sliceHeight = height / strokeCount;
        let currentSlice = 0;
        
        this.strokeCtx.clearRect(0, 0, this.strokeCanvas.width, this.strokeCanvas.height);
        
        const drawSlice = () => {
            if (currentSlice < strokeCount) {
                // Calculate source and destination rectangles
                const sourceY = (currentSlice / strokeCount) * image.height;
                const sourceHeight = image.height / strokeCount;
                
                const destY = y + (currentSlice * sliceHeight);
                
                // Draw slice
                this.strokeCtx.drawImage(
                    image,
                    0, sourceY, image.width, sourceHeight,
                    x, destY, width, sliceHeight
                );
                
                currentSlice++;
                
                // Add quantum tunneling effect occasionally
                if (currentSlice % 10 === 0) {
                    this.createQuantumTunnel(
                        x + Math.random() * width,
                        destY + Math.random() * sliceHeight
                    );
                }
                
                // Continue animation
                requestAnimationFrame(() => {
                    setTimeout(drawSlice, 10); // 10ms delay between strokes
                });
            }
        };
        
        drawSlice();
    }

    createQuantumParticles(x, y, width, height) {
        this.quantumParticles = [];
        
        // Create particles around the image
        for (let i = 0; i < 50; i++) {
            this.quantumParticles.push({
                x: x + Math.random() * width,
                y: y + Math.random() * height,
                size: Math.random() * 3 + 1,
                speedX: (Math.random() - 0.5) * 2,
                speedY: (Math.random() - 0.5) * 2,
                opacity: Math.random() * 0.5 + 0.2,
                color: `rgba(255, 215, 0, ${Math.random() * 0.3 + 0.1})`
            });
        }
        
        // Start particle animation
        this.animateQuantumParticles();
    }

    animateQuantumParticles() {
        this.strokeCtx.clearRect(0, 0, this.strokeCanvas.width, this.strokeCanvas.height);
        
        for (const particle of this.quantumParticles) {
            // Update position
            particle.x += particle.speedX;
            particle.y += particle.speedY;
            
            // Bounce off edges
            if (particle.x < 0 || particle.x > this.strokeCanvas.width) particle.speedX *= -1;
            if (particle.y < 0 || particle.y > this.strokeCanvas.height) particle.speedY *= -1;
            
            // Draw particle
            this.strokeCtx.fillStyle = particle.color;
            this.strokeCtx.beginPath();
            this.strokeCtx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            this.strokeCtx.fill();
            
            // Quantum tunneling effect (rare)
            if (Math.random() < 0.001) {
                this.createQuantumTunnel(particle.x, particle.y);
            }
        }
        
        // Continue animation
        requestAnimationFrame(() => this.animateQuantumParticles());
    }

    createQuantumTunnel(x, y) {
        // Create quantum tunnel effect
        const tunnel = document.createElement('div');
        tunnel.className = 'quantum-tunnel';
        tunnel.style.cssText = `
            position: absolute;
            left: ${x}px;
            top: ${y}px;
            width: 30px;
            height: 30px;
            background: radial-gradient(circle, rgba(255,215,0,0.6) 0%, transparent 70%);
            border-radius: 50%;
            pointer-events: none;
            z-index: 10;
            animation: tunnel-pop 0.5s ease-out forwards;
        `;
        
        document.querySelector('.canvas-container').appendChild(tunnel);
        
        // Remove after animation
        setTimeout(() => tunnel.remove(), 500);
    }

    updateQuantumState(result) {
        const stateDisplay = document.querySelector('.quantum-state-values');
        if (stateDisplay) {
            const coherence = (Math.random() * 0.2 + 0.8).toFixed(2);
            const entanglement = (Math.random() * 0.3 + 0.7).toFixed(2);
            const strokes = result.stroke_count || Math.floor(Math.random() * 5000 + 1000);
            
            stateDisplay.innerHTML = `
                <span>Coherence: ${coherence}</span>
                <span>Entanglement: ${entanglement}</span>
                <span>Strokes: ${strokes}</span>
            `;
        }
    }

    showProgress(show) {
        const progressContainer = document.querySelector('.progress-container');
        progressContainer.style.display = show ? 'block' : 'none';
    }

    updateProgress(percent) {
        const progressFill = document.querySelector('.progress-fill');
        const progressText = document.querySelector('.progress-text');
        
        if (progressFill) {
            progressFill.style.width = `${percent}%`;
        }
        
        if (progressText) {
            progressText.textContent = `${Math.round(percent)}%`;
        }
        
        this.generationProgress = percent;
    }

    showMessage(text, type) {
        const messageDiv = document.getElementById('statusMessage');
        messageDiv.textContent = text;
        messageDiv.className = `status-message status-${type}`;
        messageDiv.style.display = 'block';
        
        // Auto-hide success messages after 5 seconds
        if (type === 'success') {
            setTimeout(() => {
                messageDiv.style.display = 'none';
            }, 5000);
        }
    }

    clearAll() {
        // Clear canvases
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.strokeCtx.clearRect(0, 0, this.strokeCanvas.width, this.strokeCanvas.height);
        
        // Clear form
        document.getElementById('prompt').value = '';
        document.getElementById('referenceImage').value = '';
        document.getElementById('imagePreview').style.display = 'none';
        document.querySelector('.upload-text').textContent = 'Drag & drop or click to upload';
        document.querySelector('.upload-hint').textContent = 'Optional reference image (JPG, PNG, GIF)';
        
        // Clear quantum particles
        this.quantumParticles = [];
        
        // Reset current image
        this.currentImage = null;
        this.currentStrokes = [];
        
        // Disable download
        document.getElementById('downloadBtn').disabled = true;
        
        // Hide status message
        document.getElementById('statusMessage').style.display = 'none';
        
        console.log('Cleared all inputs and canvas');
    }

    async downloadArt() {
        if (!this.currentImage) {
            this.showMessage('No artwork to download', 'error');
            return;
        }
        
        try {
            // Create a temporary canvas for download
            const tempCanvas = document.createElement('canvas');
            const tempCtx = tempCanvas.getContext('2d');
            
            tempCanvas.width = this.currentImage.width;
            tempCanvas.height = this.currentImage.height;
            
            // Draw the image
            tempCtx.drawImage(this.currentImage, 0, 0);
            
            // Add signature
            tempCtx.font = '20px Arial';
            tempCtx.fillStyle = 'rgba(255, 215, 0, 0.7)';
            tempCtx.textAlign = 'right';
            tempCtx.fillText('Generated by Sonic AI', tempCanvas.width - 20, tempCanvas.height - 20);
            
            // Create download link
            const link = document.createElement('a');
            link.download = `sonic_ai_art_${Date.now()}.png`;
            link.href = tempCanvas.toDataURL('image/png');
            link.click();
            
            this.showMessage('Artwork downloaded successfully!', 'success');
            
        } catch (error) {
            this.showMessage('Failed to download artwork', 'error');
            console.error('Download error:', error);
        }
    }

    async loadHistory() {
        try {
            const response = await fetch('/api/artist/history?user_id=anonymous');
            const result = await response.json();
            
            if (result.success && result.artworks.length) {
                const historyGrid = document.querySelector('.history-grid');
                historyGrid.innerHTML = '';
                
                for (const artwork of result.artworks.slice(0, 6)) { // Show last 6
                    const item = document.createElement('div');
                    item.className = 'history-item';
                    item.innerHTML = `
                        <img src="data:image/png;base64,${artwork.image_data}" 
                             alt="${artwork.prompt}" 
                             class="history-image"
                             data-prompt="${artwork.prompt}"
                             data-art-type="${artwork.art_type}"
                             data-medium="${artwork.medium_style}">
                    `;
                    
                    item.addEventListener('click', () => {
                        this.loadFromHistory(artwork);
                    });
                    
                    historyGrid.appendChild(item);
                }
            }
        } catch (error) {
            console.error('Failed to load history:', error);
        }
    }

    loadFromHistory(artwork) {
        // Load prompt and settings
        document.getElementById('prompt').value = artwork.prompt;
        document.getElementById('artType').value = artwork.art_type;
        document.getElementById('mediumStyle').value = artwork.medium_style;
        
        // Display image
        this.displayGeneratedImage(artwork.image_data);
        
        // Enable download
        document.getElementById('downloadBtn').disabled = false;
        
        this.showMessage('Loaded from history', 'info');
    }

    initQuantumParticles() {
        // Create initial quantum particles in background
        const container = document.querySelector('.quantum-effects');
        if (!container) return;
        
        for (let i = 0; i < 30; i++) {
            const particle = document.createElement('div');
            particle.className = 'quantum-particle';
            particle.style.cssText = `
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                animation-delay: ${Math.random() * 3}s;
                opacity: ${Math.random() * 0.3 + 0.1};
            `;
            container.appendChild(particle);
        }
    }

    drawImage(image) {
        // Calculate scale to fit canvas
        const scale = Math.min(
            this.canvas.width / image.width,
            this.canvas.height / image.height
        );
        
        const width = image.width * scale;
        const height = image.height * scale;
        const x = (this.canvas.width - width) / 2;
        const y = (this.canvas.height - height) / 2;
        
        // Draw image
        this.ctx.drawImage(image, x, y, width, height);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.artistModule = new ArtistModule();
    
    // Add CSS for quantum tunnel animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes tunnel-pop {
            0% { transform: scale(0); opacity: 1; }
            100% { transform: scale(3); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
});