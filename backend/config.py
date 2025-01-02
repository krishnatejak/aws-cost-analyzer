import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # AWS Configuration
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    # Application Configuration
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    JWT_SECRET = os.getenv('JWT_SECRET')
    
    # API Configuration
    API_PREFIX = '/api/v1'
    
    # AWS Retry Configuration
    AWS_MAX_ATTEMPTS = int(os.getenv('AWS_MAX_ATTEMPTS', '5'))
    AWS_RETRY_MODE = os.getenv('AWS_RETRY_MODE', 'adaptive')