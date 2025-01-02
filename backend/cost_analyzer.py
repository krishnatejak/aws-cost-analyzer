import boto3
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List
import os

class AWSCostAnalyzer:
    def __init__(self):
        self.ce_client = boto3.client('ce',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION', 'us-east-1')
        )
        self.cloudwatch = boto3.client('cloudwatch',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION', 'us-east-1')
        )
        self.ec2 = boto3.client('ec2',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION', 'us-east-1')
        )
        self.rds = boto3.client('rds',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION', 'us-east-1')
        )

    def get_cost_overview(self):
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
        
        overview['services'].sort(key=lambda x: x['cost'], reverse=True)
        
        return overview