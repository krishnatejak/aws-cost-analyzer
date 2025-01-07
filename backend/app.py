from flask import Flask
from flask_cors import CORS
from src.routes.cost_routes import cost_routes
from src.routes.optimization_routes import optimization_routes

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(cost_routes)
    app.register_blueprint(optimization_routes)
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)