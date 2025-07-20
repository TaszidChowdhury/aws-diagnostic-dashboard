"""
Authentication routes for AWS Diagnostic Tool.
Handles login, logout, and user session management.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
import os

# Create blueprint
auth_bp = Blueprint('auth', __name__)

# Simple user class for authentication
class User:
    def __init__(self, username):
        self.username = username
        self.id = username
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
    
    def get_id(self):
        return self.username

# Default credentials (should be changed in production)
DEFAULT_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
DEFAULT_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.
    
    GET: Display login form
    POST: Process login credentials
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple authentication (replace with database in production)
        if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD:
            user = User(username)
            login_user(user)
            
            # Store user info in session
            session['username'] = username
            session['authenticated'] = True
            
            flash('Login successful! Welcome to AWS Diagnostic Tool.', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """
    Handle user logout.
    """
    logout_user()
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required
def profile():
    """
    Display user profile information.
    """
    return render_template('profile.html', user=current_user)

def init_auth(app):
    """
    Initialize authentication with Flask app.
    
    Args:
        app: Flask application instance
    """
    from flask_login import LoginManager
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        """Load user from session."""
        if session.get('authenticated'):
            return User(user_id)
        return None 