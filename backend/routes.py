from flask import Blueprint, jsonify
from middleware import token_required
from services.cost_service import get_cost_overview, get_cost_details, get_costs_by_service
from services.optimization_service import get_optimization_recommendations

bp = Blueprint('api', __name__, url_prefix='/api/v1')

@bp.route('/cost/overview')
@token_required
def cost_overview():
    return jsonify(get_cost_overview())

@bp.route('/cost/<time_range>')
@token_required
def cost_details(time_range):
    return jsonify(get_cost_details(time_range))

@bp.route('/cost/by-service')
@token_required
def costs_by_service():
    return jsonify(get_costs_by_service())

@bp.route('/optimization/recommendations')
@token_required
def optimization_recommendations():
    return jsonify(get_optimization_recommendations())

def init_routes(app):
    app.register_blueprint(bp)