from flask import Blueprint, jsonify
from ..cost_analyzer import AWSCostAnalyzer

cost_routes = Blueprint('cost', __name__, url_prefix='/api/v1/cost')
analyzer = AWSCostAnalyzer()

@cost_routes.route('/overview')
def get_cost_overview():
    try:
        costs = analyzer.get_cost_overview()
        return jsonify(costs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cost_routes.route('/by-service')
def get_costs_by_service():
    try:
        costs = analyzer.get_costs_by_service()
        return jsonify(costs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500