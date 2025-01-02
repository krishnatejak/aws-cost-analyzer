from flask import Blueprint, jsonify
from backend.cost_analyzer import CostAnalyzer
from backend.utils.auth import require_auth

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