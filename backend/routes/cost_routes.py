from flask import Blueprint, jsonify, request
from ..cost_analyzer import AWSCostAnalyzer

cost_routes = Blueprint('cost_routes', __name__)
cost_analyzer = AWSCostAnalyzer()

@cost_routes.route('/api/v1/cost/overview')
def get_cost_overview():
    try:
        return jsonify(cost_analyzer.get_cost_overview())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cost_routes.route('/api/v1/cost/<service>')
def get_service_costs(service):
    try:
        return jsonify(cost_analyzer.get_service_costs(service))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cost_routes.route('/api/v1/cost/trends')
def get_cost_trends():
    time_range = request.args.get('timeRange', 'month')
    try:
        return jsonify(cost_analyzer.get_cost_trends(time_range))
    except Exception as e:
        return jsonify({'error': str(e)}), 500