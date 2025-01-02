from flask import Flask
from flask_cors import CORS
from .routes import init_routes
from .config import Config

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    init_routes(app)
    return app

app = create_app()