"""
AWS Diagnostic Tool - Main Flask Application

A beginner-friendly Flask web application that simulates the tasks of a technical support analyst 
working with AWS infrastructure. This tool provides a comprehensive dashboard for monitoring and 
diagnosing AWS resources.
"""

import os
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from config import config
from routes.auth import auth_bp, init_auth
from routes.dashboard import dashboard_bp
from routes.api import api_bp
from utils.helpers import validate_aws_credentials, get_instance_state_color

def create_app(config_name='default'):
    """
    Application factory pattern for creating Flask app.
    
    Args:
        config_name: Configuration name to use
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    init_auth(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_bp)
    
    # Register template filters
    @app.template_filter('get_state_class')
    def get_state_class(state):
        """Get Bootstrap color class for instance state."""
        state_colors = {
            'running': 'success',
            'stopped': 'danger',
            'pending': 'warning',
            'terminated': 'secondary',
            'stopping': 'warning',
            'starting': 'info'
        }
        return state_colors.get(state.lower(), 'secondary')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500
    
    # Health check endpoint (no authentication required)
    @app.route('/health')
    def health_check():
        """Health check endpoint for load balancers and monitoring."""
        try:
            # Check AWS credentials
            creds_status = validate_aws_credentials()
            
            return jsonify({
                'status': 'healthy',
                'aws_credentials': creds_status['valid'],
                'timestamp': '2024-01-01T00:00:00Z'
            })
        except Exception as e:
            return jsonify({
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': '2024-01-01T00:00:00Z'
            }), 500
    
    # Root redirect
    @app.route('/')
    def index():
        """Redirect root to dashboard."""
        return redirect(url_for('dashboard.index'))
    
    return app

def main():
    """Main application entry point."""
    # Get configuration from environment
    config_name = os.environ.get('FLASK_CONFIG', 'default')
    
    # Create application
    app = create_app(config_name)
    
    # Run application
    debug = app.config.get('DEBUG', False)
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    print("=" * 60)
    print("AWS Diagnostic Tool")
    print("=" * 60)
    print(f"Configuration: {config_name}")
    print(f"Debug Mode: {debug}")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print("=" * 60)
    print("Starting application...")
    
    app.run(
        host=host,
        port=port,
        debug=debug
    )

if __name__ == '__main__':
    main() 