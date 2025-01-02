from typing import List, Dict
from datetime import datetime, timedelta

class RecommendationEngine:
    def __init__(self):
        self.service_specific_rules = {
            'EC2': self._get_ec2_recommendations,
            'RDS': self._get_rds_recommendations,
            'S3': self._get_s3_recommendations,
            'Lambda': self._get_lambda_recommendations
        }
    
    def generate_recommendations(self) -> List[Dict]:
        recommendations = []
        for service, rule_func in self.service_specific_rules.items():
            service_recommendations = rule_func()
            recommendations.extend(service_recommendations)
        return recommendations
    
    def _get_ec2_recommendations(self) -> List[Dict]:
        return [
            {
                'service': 'EC2',
                'type': 'cost_optimization',
                'title': 'Consider Graviton Migration',
                'description': 'Migrate compatible workloads to Graviton instances for up to 40% cost savings',
                'impact': 'High',
                'effort': 'Medium',
                'savings_potential': '20-40%',
                'implementation_steps': [
                    'Identify compatible workloads',
                    'Test applications on Graviton',
                    'Plan migration schedule',
                    'Monitor performance post-migration'
                ]
            },
            {
                'service': 'EC2',
                'type': 'rightsizing',
                'title': 'Instance Rightsizing Opportunity',
                'description': 'Several instances showing consistent low CPU utilization',
                'impact': 'Medium',
                'effort': 'Low',
                'savings_potential': '15-30%',
                'implementation_steps': [
                    'Review CloudWatch metrics',
                    'Identify underutilized instances',
                    'Select right-sized instance types',
                    'Schedule instance modifications'
                ]
            }
        ]
    
    def _get_rds_recommendations(self) -> List[Dict]:
        return [
            {
                'service': 'RDS',
                'type': 'modernization',
                'title': 'Evaluate Aurora Serverless v2',
                'description': 'Consider migrating compatible RDS instances to Aurora Serverless v2 for better cost optimization',
                'impact': 'High',
                'effort': 'High',
                'savings_potential': '30-50%',
                'implementation_steps': [
                    'Assess database workload patterns',
                    'Compare costs with current setup',
                    'Plan migration strategy',
                    'Test application compatibility'
                ]
            }
        ]
    
    def _get_s3_recommendations(self) -> List[Dict]:
        return [
            {
                'service': 'S3',
                'type': 'storage_optimization',
                'title': 'Optimize Storage Classes',
                'description': 'Implement lifecycle policies to move infrequently accessed data to cheaper storage tiers',
                'impact': 'Medium',
                'effort': 'Low',
                'savings_potential': '40-70%',
                'implementation_steps': [
                    'Analyze access patterns',
                    'Define lifecycle rules',
                    'Implement transitions',
                    'Monitor storage costs'
                ]
            }
        ]
    
    def _get_lambda_recommendations(self) -> List[Dict]:
        return [
            {
                'service': 'Lambda',
                'type': 'performance_optimization',
                'title': 'Optimize Lambda Memory Settings',
                'description': 'Adjust memory settings based on function execution patterns',
                'impact': 'Low',
                'effort': 'Low',
                'savings_potential': '10-20%',
                'implementation_steps': [
                    'Review execution metrics',
                    'Test different memory configurations',
                    'Update function settings',
                    'Monitor performance impact'
                ]
            }
        ]