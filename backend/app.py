from flask import Flask
from flask_cors import CORS
from routes import init_routes
from config import Config

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    init_routes(app)

    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)