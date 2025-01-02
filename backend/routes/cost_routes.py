from flask import Blueprint, jsonify
from ..cost_analyzer import CostAnalyzer
from ..utils.auth import require_auth

cost_routes = Blueprint('cost_routes', __name__)
cost_analyzer = CostAnalyzer()

@cost_routes.route('/api/costs/overview', methods=['GET'])
@require_auth
def get_cost_overview():
    try:
        overview = cost_analyzer.get_cost_overview()
        return jsonify(overview)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cost_routes.route('/api/costs/by-service', methods=['GET'])
@require_auth
def get_costs_by_service():
    try:
        service_costs = cost_analyzer.get_costs_by_service()
        return jsonify(service_costs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cost_routes.route('/api/costs/recommendations', methods=['GET'])
@require_auth
def get_cost_recommendations():
    try:
        recommendations = cost_analyzer.get_cost_recommendations()
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500