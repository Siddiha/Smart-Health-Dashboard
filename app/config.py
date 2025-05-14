import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    """Base configuration class."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    MONGO_URI = os.getenv('MONGO_URI')
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

# Map environment names to config objects
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# Get current configuration
def get_config():
    """Return the appropriate configuration object based on the environment variable."""
    env = os.getenv('FLASK_ENV', 'development')
    return config_by_name.get(env, config_by_name['default'])