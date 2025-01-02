from flask import Flask
from flask_cors import CORS
from config import Config
from routes import init_routes
from utils.logger import setup_logger
import boto3
import os

# Initialize logger
logger = setup_logger(__name__, Config.LOG_LEVEL)

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize AWS session
    if app.config['AWS_PROFILE']:
        boto3.setup_default_session(profile_name=app.config['AWS_PROFILE'])
    
    # Register routes
    init_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=Config.DEBUG
    )