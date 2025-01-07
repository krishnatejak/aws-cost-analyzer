from flask import Blueprint, jsonify
from ..cost_analyzer import AWSCostAnalyzer

optimization_routes = Blueprint('optimization', __name__, url_prefix='/api/v1/optimization')
analyzer = AWSCostAnalyzer()

@optimization_routes.route('/recommendations')
def get_recommendations():
    try:
        recommendations = analyzer.get_optimization_recommendations()
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500