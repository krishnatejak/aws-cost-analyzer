import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    AWS_PROFILE = os.getenv('AWS_PROFILE', 'default')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # API Configuration
    API_PREFIX = '/api/v1'
    
    # AWS Retry Configuration
    AWS_MAX_ATTEMPTS = int(os.getenv('AWS_MAX_ATTEMPTS', '5'))
    AWS_RETRY_MODE = os.getenv('AWS_RETRY_MODE', 'adaptive')