from flask import Blueprint, jsonify, request
from ..service_analyzers import EC2Analyzer, RDSAnalyzer, StorageAnalyzer, NetworkAnalyzer
from ..utils.logger import get_logger

logger = get_logger(__name__)
optimization_bp = Blueprint('optimization', __name__)

@optimization_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    try:
        # Initialize analyzers
        ec2_analyzer = EC2Analyzer()
        rds_analyzer = RDSAnalyzer()
        storage_analyzer = StorageAnalyzer()
        network_analyzer = NetworkAnalyzer()
        
        # Gather recommendations
        recommendations = {
            'ec2': ec2_analyzer.get_cost_optimization_recommendations(),
            'rds': rds_analyzer.get_optimization_recommendations(),
            'storage': storage_analyzer.get_optimization_recommendations(),
            'network': network_analyzer.get_recommendations()
        }
        
        return jsonify(recommendations)
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        return jsonify({'error': 'Failed to get recommendations'}), 500

@optimization_bp.route('/service/<service_name>', methods=['GET'])
def get_service_recommendations(service_name):
    try:
        if service_name == 'ec2':
            analyzer = EC2Analyzer()
            recommendations = analyzer.get_cost_optimization_recommendations()
        elif service_name == 'rds':
            analyzer = RDSAnalyzer()
            recommendations = analyzer.get_optimization_recommendations()
        elif service_name == 'storage':
            analyzer = StorageAnalyzer()
            recommendations = analyzer.get_optimization_recommendations()
        elif service_name == 'network':
            analyzer = NetworkAnalyzer()
            recommendations = analyzer.get_recommendations()
        else:
            return jsonify({'error': 'Invalid service name'}), 400
            
        return jsonify(recommendations)
    except Exception as e:
        logger.error(f"Error getting recommendations for service {service_name}: {str(e)}")
        return jsonify({'error': f'Failed to get recommendations for {service_name}'}), 500

@optimization_bp.route('/savings-plan', methods=['GET'])
def get_savings_plan_recommendations():
    try:
        ec2_analyzer = EC2Analyzer()
        rds_analyzer = RDSAnalyzer()
        
        # Get compute usage for both EC2 and RDS
        ec2_usage = ec2_analyzer.get_utilization_metrics()
        rds_usage = rds_analyzer.get_instance_metrics()
        
        # Calculate optimal savings plan
        recommendations = {
            'compute_savings_plan': _calculate_compute_savings_plan(ec2_usage, rds_usage),
            'ec2_instance_savings_plan': _calculate_ec2_savings_plan(ec2_usage),
            'potential_savings': _calculate_potential_savings(ec2_usage, rds_usage)
        }
        
        return jsonify(recommendations)
    except Exception as e:
        logger.error(f"Error getting savings plan recommendations: {str(e)}")
        return jsonify({'error': 'Failed to get savings plan recommendations'}), 500

def _calculate_compute_savings_plan(ec2_usage, rds_usage):
    # Calculate optimal compute savings plan based on usage patterns
    total_compute_usage = sum(instance['metrics']['cpu']['average'] 
                             for instance in ec2_usage + rds_usage)
    
    return {
        'recommended_commitment': total_compute_usage * 0.7,  # 70% of total usage
        'term_length': '1 year' if total_compute_usage < 1000 else '3 year',
        'payment_option': 'Partial Upfront',
        'estimated_savings_percentage': '30-40%'
    }

def _calculate_ec2_savings_plan(ec2_usage):
    # Calculate EC2 instance specific savings plan
    instance_usage = {}
    for instance in ec2_usage:
        instance_type = instance['instance_type']
        if instance_type not in instance_usage:
            instance_usage[instance_type] = 0
        instance_usage[instance_type] += 1
    
    return {
        'instance_recommendations': [
            {
                'instance_type': instance_type,
                'current_count': count,
                'recommended_commitment': count * 0.8,  # 80% commitment
                'estimated_savings': '25-35%'
            }
            for instance_type, count in instance_usage.items()
        ]
    }

def _calculate_potential_savings(ec2_usage, rds_usage):
    # Calculate potential savings across different commitment options
    total_instances = len(ec2_usage) + len(rds_usage)
    
    return {
        'no_upfront_1_year': {
            'commitment_required': 0,
            'estimated_monthly_savings': total_instances * 100,  # Example calculation
            'savings_percentage': '20%'
        },
        'partial_upfront_1_year': {
            'commitment_required': total_instances * 1000,
            'estimated_monthly_savings': total_instances * 150,
            'savings_percentage': '30%'
        },
        'all_upfront_1_year': {
            'commitment_required': total_instances * 2000,
            'estimated_monthly_savings': total_instances * 200,
            'savings_percentage': '40%'
        },
        'partial_upfront_3_year': {
            'commitment_required': total_instances * 2500,
            'estimated_monthly_savings': total_instances * 250,
            'savings_percentage': '50%'
        }
    }