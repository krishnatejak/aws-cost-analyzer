from flask import Blueprint
from .cost_routes import cost_routes

def init_routes(app):
    app.register_blueprint(cost_routes)