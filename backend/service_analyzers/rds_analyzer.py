import boto3
import os
from datetime import datetime, timedelta

class RDSAnalyzer:
    def __init__(self):
        self.rds = boto3.client('rds',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION', 'us-east-1')
        )
        self.cloudwatch = boto3.client('cloudwatch')
        self.ce = boto3.client('ce')

    def analyze(self):
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

        instances = self.rds.describe_db_instances()
        cost_data = self.ce.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            Filter={
                'Dimensions': {
                    'Key': 'SERVICE',
                    'Values': ['Amazon Relational Database Service']
                }
            }
        )

        analysis = {
            'total_instances': 0,
            'total_cost': 0,
            'engine_types': {},
            'instances': [],
            'optimization_opportunities': []
        }

        # Calculate total cost
        for result in cost_data['ResultsByTime']:
            analysis['total_cost'] += float(result['Total']['UnblendedCost']['Amount'])

        for instance in instances['DBInstances']:
            analysis['total_instances'] += 1
            engine = instance['Engine']
            analysis['engine_types'][engine] = analysis['engine_types'].get(engine, 0) + 1

            # Get instance metrics
            metrics = self._get_instance_metrics(instance['DBInstanceIdentifier'])

            instance_data = {
                'identifier': instance['DBInstanceIdentifier'],
                'engine': engine,
                'status': instance['DBInstanceStatus'],
                'size': instance['DBInstanceClass'],
                'storage': instance['AllocatedStorage'],
                'multi_az': instance.get('MultiAZ', False),
                'metrics': metrics
            }
            analysis['instances'].append(instance_data)

            # Check for optimization opportunities
            self._check_optimization_opportunities(instance, metrics, analysis)

        return analysis

    def _get_instance_metrics(self, instance_id, days=7):
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days)

        metrics = {}
        for metric_name in ['CPUUtilization', 'DatabaseConnections', 'FreeStorageSpace']:
            response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/RDS',
                MetricName=metric_name,
                Dimensions=[{'Name': 'DBInstanceIdentifier', 'Value': instance_id}],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,
                Statistics=['Average', 'Maximum']
            )

            if response['Datapoints']:
                metrics[metric_name] = {
                    'average': sum(p['Average'] for p in response['Datapoints']) / len(response['Datapoints']),
                    'max': max(p['Maximum'] for p in response['Datapoints'])
                }

        return metrics

    def _check_optimization_opportunities(self, instance, metrics, analysis):
        # Check CPU utilization
        if metrics.get('CPUUtilization', {}).get('average', 0) < 20:
            analysis['optimization_opportunities'].append({
                'instance_id': instance['DBInstanceIdentifier'],
                'type': 'Low CPU Utilization',
                'description': 'Consider downsizing instance due to low CPU usage',
                'current_value': f"{metrics['CPUUtilization']['average']:.1f}%"
            })

        # Check storage utilization
        if 'FreeStorageSpace' in metrics:
            total_storage = instance['AllocatedStorage'] * 1024 * 1024 * 1024  # Convert GB to bytes
            free_storage = metrics['FreeStorageSpace']['average']
            used_percentage = ((total_storage - free_storage) / total_storage) * 100

            if used_percentage < 30:
                analysis['optimization_opportunities'].append({
                    'instance_id': instance['DBInstanceIdentifier'],
                    'type': 'Low Storage Utilization',
                    'description': 'Consider reducing allocated storage',
                    'current_value': f"{used_percentage:.1f}% used"
                })

        # Check Multi-AZ usage
        if instance.get('MultiAZ', False) and metrics.get('DatabaseConnections', {}).get('max', 0) < 100:
            analysis['optimization_opportunities'].append({
                'instance_id': instance['DBInstanceIdentifier'],
                'type': 'Multi-AZ Review',
                'description': 'Low connection count with Multi-AZ enabled',
                'current_value': f"{metrics.get('DatabaseConnections', {}).get('max', 0)} max connections"
            })
