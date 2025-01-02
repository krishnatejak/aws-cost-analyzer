from flask import Blueprint, jsonify
from ..service_analyzers import EC2Analyzer, RDSAnalyzer

service_routes = Blueprint('service_routes', __name__)

@service_routes.route('/api/v1/services/ec2')
def get_ec2_analysis():
    try:
        analyzer = EC2Analyzer()
        return jsonify(analyzer.analyze())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@service_routes.route('/api/v1/services/rds')
def get_rds_analysis():
    try:
        analyzer = RDSAnalyzer()
        return jsonify(analyzer.analyze())
    except Exception as e:
        return jsonify({'error': str(e)}), 500