from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def create_app():
    """Initialize the Flask application."""
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')
    
    # Import and register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app