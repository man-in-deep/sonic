import os
import logging
import json
import uuid
import base64
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, jsonify, request, send_from_directory, session
from config import config
from datetime import datetime
from io import BytesIO
from PIL import Image
import numpy as np

# NEW IMPORTS for Phase 2
from artist_module.services import AIService
from artist_module.quantum_simulator import QuantumStrokeSimulator
from artist_module.utils import ImageProcessor, DatabaseManager

def create_app(config_name='default'):
    """Application factory function"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Setup logging
    setup_logging(app)
    
    # Create necessary directories
    create_directories(app)
    
    # NEW: Initialize Phase 2 services
    init_artist_services(app)
    
    # Register routes
    register_routes(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register context processors
    register_context_processors(app)
    
    return app

def setup_logging(app):
    """Configure logging for the application"""
    if not os.path.exists(app.config['LOG_FOLDER']):
        os.makedirs(app.config['LOG_FOLDER'])
    
    log_file = os.path.join(app.config['LOG_FOLDER'], app.config['LOG_FILE'])
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    # Set log level
    file_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))
    
    # Add handler to app logger
    app.logger.addHandler(file_handler)
    app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))
    
    # Log application start
    app.logger.info('Sonic AI Application Starting...')
    app.logger.info(f'Environment: {app.config["ENV"]}')
    app.logger.info(f'Debug Mode: {app.config["DEBUG"]}')

def create_directories(app):
    """Create necessary directories"""
    directories = [
        app.config['UPLOAD_FOLDER'],
        'static/videos',
        'static/images',
        'static/js',
        'static/css',
        'uploads/artist',  # NEW: Artist uploads directory
        'uploads/generated'  # NEW: Generated images directory
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            app.logger.info(f'Created directory: {directory}')

# NEW: Initialize artist services
def init_artist_services(app):
    """Initialize Phase 2 artist services"""
    try:
        # Initialize AI service
        app.ai_service = AIService()
        app.logger.info('AI Service initialized successfully')
        
        # Initialize quantum simulator
        app.quantum_simulator = QuantumStrokeSimulator()
        app.logger.info('Quantum Stroke Simulator initialized')
        
        # Initialize database manager
        app.db_manager = DatabaseManager()
        app.logger.info('Database Manager initialized')
        
        # Initialize image processor
        app.image_processor = ImageProcessor()
        app.logger.info('Image Processor initialized')
        
    except Exception as e:
        app.logger.error(f'Failed to initialize artist services: {e}')
        # Set None if initialization fails
        app.ai_service = None
        app.quantum_simulator = None
        app.db_manager = None
        app.image_processor = None

def register_routes(app):
    """Register application routes"""
    
    @app.route('/')
    def index():
        """Main landing page"""
        app.logger.info('Accessed landing page')
        return render_template('index.html')
    
    @app.route('/artist')
    def artist():
        """Artist module page (Phase 2)"""
        app.logger.info('Accessed artist module')
        return render_template('artist.html')
    
    @app.route('/poet')
    def poet():
        """Poet module page (Phase 3)"""
        app.logger.info('Accessed poet module')
        return render_template('poet.html')
    
    @app.route('/author')
    def author():
        """Author module page (Phase 4)"""
        app.logger.info('Accessed author module')
        return render_template('author.html')
    
    # NEW: Phase 2 API Routes
    @app.route('/api/artist/generate', methods=['POST'])
    def generate_art():
        """Generate art based on user input"""
        try:
            # Get form data
            prompt = request.form.get('prompt', '')
            art_type = request.form.get('art_type', 'Realism')
            medium_style = request.form.get('medium_style', 'Digital Painting')
            
            if not prompt:
                return jsonify({'success': False, 'error': 'Prompt is required'})
            
            # Check if services are initialized
            if not app.ai_service:
                return jsonify({'success': False, 'error': 'AI service not initialized'})
            
            # Handle reference image (optional)
            reference_image = None
            reference_path = None
            
            if 'reference_image' in request.files:
                file = request.files['reference_image']
                if file and file.filename:
                    if app.image_processor.validate_image(file):
                        # Save reference image
                        reference_path = app.image_processor.save_uploaded_file(
                            file, 'uploads/artist'
                        )
                        # Resize if needed
                        reference_path = app.image_processor.resize_image(reference_path)
                        
                        # Open as PIL Image
                        reference_image = Image.open(reference_path)
                    else:
                        return jsonify({'success': False, 'error': 'Invalid image format'})
            
            # Generate art
            result = app.ai_service.generate_art(
                prompt=prompt,
                art_type=art_type,
                medium_style=medium_style,
                reference_image=reference_image
            )
            
            if not result['success']:
                return jsonify(result)
            
            # Save generated image
            image_data = base64.b64decode(result['image_data'])
            image_filename = f"{uuid.uuid4().hex}.png"
            image_path = os.path.join('uploads/generated', image_filename)
            
            with open(image_path, 'wb') as f:
                f.write(image_data)
            
            # Generate stroke simulation
            stroke_image_data = None
            stroke_count = 0
            
            if app.quantum_simulator:
                try:
                    # Open generated image for stroke simulation
                    generated_image = Image.open(BytesIO(image_data))
                    
                    # Plan strokes
                    strokes = app.quantum_simulator.plan_strokes(
                        generated_image, art_type, medium_style
                    )
                    
                    # Convert strokes to JSON serializable format
                    serializable_strokes = []
                    for stroke in strokes:
                        # Convert numpy types to Python native types
                        serializable_stroke = {}
                        for key, value in stroke.items():
                            if isinstance(value, np.integer):
                                serializable_stroke[key] = int(value)
                            elif isinstance(value, np.floating):
                                serializable_stroke[key] = float(value)
                            elif isinstance(value, np.ndarray):
                                serializable_stroke[key] = value.tolist()
                            elif key == 'color' and isinstance(value, tuple):
                                # Convert color tuple to list
                                serializable_stroke[key] = list(value)
                            else:
                                serializable_stroke[key] = value
                        serializable_strokes.append(serializable_stroke)
                    
                    # Simulate stroke rendering
                    stroke_image = app.quantum_simulator.simulate_stroke_rendering(
                        generated_image, serializable_strokes
                    )
                    
                    # Save stroke simulation
                    stroke_filename = f"stroke_{uuid.uuid4().hex}.png"
                    stroke_path = os.path.join('uploads/generated', stroke_filename)
                    stroke_image.save(stroke_path)
                    
                    stroke_image_data = app.image_processor.image_to_base64(stroke_path)
                    stroke_count = len(serializable_strokes)
                    
                except Exception as e:
                    app.logger.error(f"Error in stroke simulation: {str(e)}")
                    # Continue without stroke simulation if it fails
            
            # Save to database
            if app.db_manager:
                try:
                    artwork_data = {
                        'user_id': session.get('user_id', 'anonymous'),
                        'user_prompt': prompt,
                        'reference_image_path': reference_path,
                        'art_type': art_type,
                        'medium_style': medium_style,
                        'model_used': result['model_used'],
                        'stroke_sequence': json.dumps([]),  # Empty for now
                        'generation_parameters': json.dumps({
                            'steps': 30,
                            'guidance_scale': 7.5,
                            'seed': -1
                        }),
                        'image_path': image_path,
                        'creation_duration': result['generation_time']
                    }
                    
                    app.db_manager.save_artwork(artwork_data)
                except Exception as e:
                    app.logger.error(f"Error saving to database: {str(e)}")
                    # Continue even if database save fails
            
            # Return success response
            response_data = {
                'success': True,
                'image_data': result['image_data'],
                'stroke_data': stroke_image_data,
                'model_used': result['model_used'],
                'generation_time': result['generation_time'],
                'stroke_count': stroke_count,
                'art_type': art_type,
                'medium_style': medium_style
            }
            
            return jsonify(response_data)
            
        except Exception as e:
            app.logger.error(f"Error generating art: {str(e)}")
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/api/artist/history', methods=['GET'])
    def get_art_history():
        """Get user's art generation history"""
        try:
            user_id = request.args.get('user_id', 'anonymous')
            
            if app.db_manager:
                history = app.db_manager.get_artwork_history(user_id, limit=20)
                
                # Convert to response format
                artworks = []
                for item in history:
                    if item.get('image_path') and os.path.exists(item['image_path']):
                        try:
                            with open(item['image_path'], 'rb') as f:
                                image_data = base64.b64encode(f.read()).decode()
                            
                            artworks.append({
                                'id': str(item.get('id', '')),
                                'prompt': item.get('user_prompt', ''),
                                'art_type': item.get('art_type', ''),
                                'medium_style': item.get('medium_style', ''),
                                'created_at': item.get('created_at').isoformat() if item.get('created_at') else None,
                                'image_data': image_data
                            })
                        except Exception as e:
                            app.logger.error(f"Error reading image file {item.get('image_path')}: {str(e)}")
                            continue
                
                return jsonify({'success': True, 'artworks': artworks})
            else:
                return jsonify({'success': False, 'error': 'Database not available'})
                
        except Exception as e:
            app.logger.error(f"Error fetching art history: {str(e)}")
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/api/artist/download/<filename>')
    def download_artwork(filename):
        """Download generated artwork"""
        try:
            filepath = os.path.join('uploads/generated', filename)
            if os.path.exists(filepath):
                return send_from_directory('uploads/generated', filename, as_attachment=True)
            else:
                return jsonify({'success': False, 'error': 'File not found'})
        except Exception as e:
            app.logger.error(f"Error downloading artwork: {str(e)}")
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/api/quantum-state', methods=['GET'])
    def get_quantum_state():
        """API endpoint for quantum simulation data"""
        import random
        
        state = {
            'coherence': random.uniform(0.7, 0.99),
            'entanglement': random.uniform(0.5, 0.95),
            'tunneling_probability': app.config['QUANTUM_TUNNELING_PROBABILITY'],
            'decay_rate': app.config['QUANTUM_DECAY_RATE'],
            'timestamp': datetime.now().isoformat(),
            'particles': random.randint(50, 200)
        }
        
        app.logger.debug(f'Quantum state requested: {state}')
        return jsonify(state)
    
    @app.route('/api/trail-data', methods=['POST'])
    def save_trail_data():
        """Save pencil trail data (for future analysis)"""
        data = request.json
        app.logger.debug(f'Trail data received: {len(data.get("trails", []))} trails')
        
        # In Phase 1, just log it. In later phases, save to database
        return jsonify({'status': 'success', 'message': 'Trail data logged'})
    
    @app.route('/static/<path:filename>')
    def serve_static(filename):
        """Serve static files"""
        return send_from_directory('static', filename)
    
    @app.route('/favicon.ico')
    def favicon():
        """Serve favicon"""
        return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

def register_error_handlers(app):
    """Register error handlers"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.warning(f'404 error: {request.path}')
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'500 error: {error}')
        return render_template('500.html'), 500

def register_context_processors(app):
    """Register context processors for template variables"""
    
    @app.context_processor
    def inject_now():
        """Inject current datetime into templates"""
        return {'now': datetime.now()}
    
    @app.context_processor
    def inject_config():
        """Inject configuration into templates"""
        return {
            'app_name': app.config['APP_NAME'],
            'app_version': app.config['APP_VERSION']
        }
    
    # NEW: Inject art types and medium styles for templates
    @app.context_processor
    def inject_artist_data():
        """Inject artist module data"""
        return {
            'art_types': [
                'Impressionism', 'Cubism', 'Expressionism', 'Surrealism',
                'Pop Art', 'Realism', 'Abstract Expressionism', 'Modernism/Contemporary'
            ],
            'medium_styles': [
                'Oil Paint', 'Acrylic Paint', 'Watercolor', 'Gouache',
                'Pastels', 'Tempera', 'Encaustic', 'Fresco',
                'Ink Painting', 'Pencil Art', 'Digital Painting'
            ]
        }

if __name__ == '__main__':
    # Create application instance
    app = create_app()
    
    # Run the application
    app.logger.info('Starting Sonic AI Flask server...')
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG'],
        threaded=True
    )