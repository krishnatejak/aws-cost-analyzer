import boto3
from datetime import datetime, timedelta
from .config import AWS_CONFIG

class AWSCostAnalyzer:
    def __init__(self):
        self.ce_client = boto3.client('ce', **AWS_CONFIG)
        self.cloudwatch = boto3.client('cloudwatch', **AWS_CONFIG)
        self.ec2 = boto3.client('ec2', **AWS_CONFIG)
        self.rds = boto3.client('rds', **AWS_CONFIG)
        
    def get_cost_overview(self, start_date=None, end_date=None):
        if not start_date:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
        response = self.ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date.strftime('%Y-%m-%d'),
                'End': end_date.strftime('%Y-%m-%d')
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost']
        )
        return response
        
    def get_costs_by_service(self):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        response = self.ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date.strftime('%Y-%m-%d'),
                'End': end_date.strftime('%Y-%m-%d')
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        )
        return response

    def get_optimization_recommendations(self):
        # Sample recommendation logic - replace with actual implementation
        recommendations = [
            {
                'title': 'Underutilized EC2 Instances',
                'description': 'Consider downsizing or terminating instances with low CPU utilization',
                'potentialSavings': 120.50
            },
            {
                'title': 'Unused EBS Volumes',
                'description': 'Remove unattached EBS volumes',
                'potentialSavings': 45.20
            }
        ]
        return recommendations