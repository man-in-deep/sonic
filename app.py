import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, jsonify, request, send_from_directory
from config import config
from datetime import datetime

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
        'static/css'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            app.logger.info(f'Created directory: {directory}')

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
        return render_template('artist.html')  # Will be created in Phase 2
    
    @app.route('/poet')
    def poet():
        """Poet module page (Phase 3)"""
        app.logger.info('Accessed poet module')
        return render_template('poet.html')  # Will be created in Phase 3
    
    @app.route('/author')
    def author():
        """Author module page (Phase 4)"""
        app.logger.info('Accessed author module')
        return render_template('author.html')  # Will be created in Phase 4
    
    @app.route('/api/quantum-state', methods=['GET'])
    def get_quantum_state():
        """API endpoint for quantum simulation data"""
        import random
        import time
        
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