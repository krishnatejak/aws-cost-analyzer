from flask import Blueprint, jsonify, request
from ..service_analyzers import EC2Analyzer, RDSAnalyzer, StorageAnalyzer, NetworkAnalyzer
from ..utils.logger import get_logger
from ..utils.validators import validate_date_format, validate_date_range, require_params

logger = get_logger(__name__)
cost_bp = Blueprint('cost', __name__)

@cost_bp.route('/overview', methods=['GET'])
def get_cost_overview():
    try:
        # Initialize analyzers
        ec2_analyzer = EC2Analyzer()
        rds_analyzer = RDSAnalyzer()
        storage_analyzer = StorageAnalyzer()
        network_analyzer = NetworkAnalyzer()
        
        # Gather cost data
        cost_data = {
            'ec2': ec2_analyzer.analyze_instance_types(),
            'rds': rds_analyzer.analyze_all_databases(),
            'storage': storage_analyzer.analyze_storage(),
            'network': network_analyzer.analyze_network_costs()
        }
        
        return jsonify(cost_data)
    except Exception as e:
        logger.error(f"Error getting cost overview: {str(e)}")
        return jsonify({'error': 'Failed to get cost overview'}), 500

@cost_bp.route('/service/<service_name>', methods=['GET'])
def get_service_costs(service_name):
    if service_name not in ['ec2', 'rds', 'storage', 'network']:
        return jsonify({'error': 'Invalid service name'}), 400
        
    try:
        if service_name == 'ec2':
            analyzer = EC2Analyzer()
            data = analyzer.analyze_instance_types()
        elif service_name == 'rds':
            analyzer = RDSAnalyzer()
            data = analyzer.analyze_all_databases()
        elif service_name == 'storage':
            analyzer = StorageAnalyzer()
            data = analyzer.analyze_storage()
        else:  # network
            analyzer = NetworkAnalyzer()
            data = analyzer.analyze_network_costs()
            
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error getting costs for service {service_name}: {str(e)}")
        return jsonify({'error': f'Failed to get costs for {service_name}'}), 500

@cost_bp.route('/trends', methods=['GET'])
@require_params('start_date', 'end_date')
def get_cost_trends():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    granularity = request.args.get('granularity', 'MONTHLY')
    
    # Validate date formats
    valid, error = validate_date_format(start_date)
    if not valid:
        return jsonify({'error': error}), 400
        
    valid, error = validate_date_format(end_date)
    if not valid:
        return jsonify({'error': error}), 400
        
    # Validate date range
    valid, error = validate_date_range(start_date, end_date)
    if not valid:
        return jsonify({'error': error}), 400
        
    # Validate granularity
    if granularity not in ['DAILY', 'MONTHLY']:
        return jsonify({'error': 'Invalid granularity. Must be DAILY or MONTHLY'}), 400
    
    try:
        # Initialize analyzers
        ec2_analyzer = EC2Analyzer()
        rds_analyzer = RDSAnalyzer()
        
        # Get trends for each service
        trends = {
            'ec2': ec2_analyzer.get_cost_trends(start_date, end_date, granularity),
            'rds': rds_analyzer.get_cost_trends(start_date, end_date, granularity)
        }
        
        return jsonify(trends)
    except Exception as e:
        logger.error(f"Error getting cost trends: {str(e)}")
        return jsonify({'error': 'Failed to get cost trends'}), 500