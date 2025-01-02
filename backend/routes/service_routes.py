from flask import Blueprint, jsonify
from ..service_analyzers import EC2Analyzer, RDSAnalyzer, StorageAnalyzer, NetworkAnalyzer
from ..utils.auth import require_auth

service_routes = Blueprint('service_routes', __name__)

@service_routes.route('/api/v1/services/ec2/instances', methods=['GET'])
@require_auth
def get_ec2_analysis():
    analyzer = EC2Analyzer()
    return jsonify(analyzer.analyze())

@service_routes.route('/api/v1/services/rds/instances', methods=['GET'])
@require_auth
def get_rds_analysis():
    analyzer = RDSAnalyzer()
    return jsonify(analyzer.analyze())