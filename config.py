"""
Configuration settings for the Media Scraper API
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    API_SECRET_KEY = os.getenv('API_SECRET_KEY', 'robins_secret_key_2024')
    
    # Flask settings
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Server settings
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 12000))
    
    # Scraper settings
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 30))
    MAX_FORMATS = int(os.getenv('MAX_FORMATS', 50))
    
    # Rate limiting (if needed in future)
    RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', 60))


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_DEBUG = False
    
    # Override with production values
    API_SECRET_KEY = os.getenv('API_SECRET_KEY')
    if not API_SECRET_KEY:
        raise ValueError("API_SECRET_KEY must be set in production")


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    API_SECRET_KEY = 'test-api-key'


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}