from flask import Blueprint
from .cost_routes import cost_routes
from .service_routes import service_routes
from .optimization_routes import optimization_routes

def init_routes(app):
    app.register_blueprint(cost_routes)
    app.register_blueprint(service_routes)
    app.register_blueprint(optimization_routes)