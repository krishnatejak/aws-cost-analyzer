from flask import Blueprint, jsonify
from ..cost_optimizer import CostOptimizer

optimization_routes = Blueprint('optimization_routes', __name__)
optimizer = CostOptimizer()

@optimization_routes.route('/api/v1/optimization/recommendations')
def get_recommendations():
    try:
        return jsonify(optimizer.get_recommendations())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@optimization_routes.route('/api/v1/optimization/overview')
def get_savings_overview():
    try:
        return jsonify(optimizer.get_savings_overview())
    except Exception as e:
        return jsonify({'error': str(e)}), 500