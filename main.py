from flask import Flask, render_template, jsonify
from config import config
import os

def create_app(config_name=None):
    """Application factory pattern"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions (will add later)
    # db.init_app(app)
    # init_firebase(app)
    
    # Register blueprints (will add later)
    # from routes.auth import auth_bp
    # app.register_blueprint(auth_bp)
    
    # Basic routes
    @app.route('/')
    def index():
        """Home page"""
        return render_template('index.html')
    
    @app.route('/health')
    def health_check():
        """Health check endpoint for monitoring"""
        return jsonify({
            'status': 'healthy',
            'service': 'tastehub',
            'version': '1.0.0'
        }), 200
    
    @app.errorhandler(404)
    def not_found(error):
        """404 error handler"""
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """500 error handler"""
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

# For local development
if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=8080, debug=True)