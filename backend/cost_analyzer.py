import boto3
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List

class AWSCostAnalyzer:
    def __init__(self):
        self.ce_client = boto3.client('ce')
        self.cloudwatch = boto3.client('cloudwatch')
        self.ec2 = boto3.client('ec2')
        self.rds = boto3.client('rds')
    
    def get_cost_overview(self):
        # Get cost data for the last 30 days
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        response = self.ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='DAILY',
            Metrics=['UnblendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        )
        
        # Process the data
        overview = {
            'total_cost': 0,
            'services': [],
            'daily_costs': []
        }
        
        for result in response['ResultsByTime']:
            daily_cost = 0
            for group in result['Groups']:
                cost = float(group['Metrics']['UnblendedCost']['Amount'])
                daily_cost += cost
                
                # Add to services list if not exists
                service = group['Keys'][0]
                service_found = False
                for s in overview['services']:
                    if s['name'] == service:
                        s['cost'] += cost
                        service_found = True
                        break
                if not service_found:
                    overview['services'].append({
                        'name': service,
                        'cost': cost
                    })
            
            overview['daily_costs'].append({
                'date': result['TimePeriod']['Start'],
                'cost': daily_cost
            })
            overview['total_cost'] += daily_cost
        
        # Sort services by cost
        overview['services'].sort(key=lambda x: x['cost'], reverse=True)
        
        return overview
    
    def get_cost_and_usage(self, start_date=None, end_date=None):
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
            
        response = self.ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='DAILY',
            Metrics=['UnblendedCost', 'UsageQuantity'],
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'SERVICE'},
                {'Type': 'TAG', 'Key': 'Environment'}
            ]
        )
        return response
    
    def get_ec2_utilization(self):
        instances = self.ec2.describe_instances()
        metrics = []
        
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                
                # Get CPU utilization
                response = self.cloudwatch.get_metric_statistics(
                    Namespace='AWS/EC2',
                    MetricName='CPUUtilization',
                    Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                    StartTime=datetime.utcnow() - timedelta(days=14),
                    EndTime=datetime.utcnow(),
                    Period=3600,
                    Statistics=['Average']
                )
                
                metrics.append({
                    'InstanceId': instance_id,
                    'InstanceType': instance['InstanceType'],
                    'CPUUtilization': response['Datapoints']
                })
        
        return metrics
    
    def get_rds_utilization(self):
        instances = self.rds.describe_db_instances()
        metrics = []
        
        for instance in instances['DBInstances']:
            instance_id = instance['DBInstanceIdentifier']
            
            # Get CPU utilization
            response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/RDS',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'DBInstanceIdentifier', 'Value': instance_id}],
                StartTime=datetime.utcnow() - timedelta(days=14),
                EndTime=datetime.utcnow(),
                Period=3600,
                Statistics=['Average']
            )
            
            metrics.append({
                'DBInstanceIdentifier': instance_id,
                'DBInstanceClass': instance['DBInstanceClass'],
                'CPUUtilization': response['Datapoints']
            })
        
        return metrics