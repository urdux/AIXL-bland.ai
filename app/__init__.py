from flask import Flask
from app.config import Config
from app.database import db, create_database, init_app
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from .routes.campaign import campaign_bp
# Import blueprints
from app.routes.auth import auth_bp
from app.routes.users import users_bp
from app.models.user import User  # Import User model for user_loader

csrf = CSRFProtect()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    create_database()  # Create the database if it doesn’t exist
    init_app(app)      # Initialize db and tables with the app

    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(campaign_bp, url_prefix='/campaigns')

    return app

# Define user_loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
