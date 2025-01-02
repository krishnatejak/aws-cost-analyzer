import boto3
import os
from datetime import datetime, timedelta

class EC2Analyzer:
    def __init__(self):
        self.ec2 = boto3.client('ec2',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION', 'us-east-1')
        )
        self.cloudwatch = boto3.client('cloudwatch')
        self.ce = boto3.client('ce')

    def analyze(self):
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

        instances = self.ec2.describe_instances()
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
                    'Values': ['Amazon Elastic Compute Cloud - Compute']
                }
            }
        )

        analysis = {
            'total_instances': 0,
            'total_cost': 0,
            'running_instances': 0,
            'stopped_instances': 0,
            'instance_types': {},
            'instances': [],
            'optimization_opportunities': []
        }

        # Calculate total cost
        for result in cost_data['ResultsByTime']:
            analysis['total_cost'] += float(result['Total']['UnblendedCost']['Amount'])

        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                analysis['total_instances'] += 1
                instance_state = instance['State']['Name']
                instance_type = instance['InstanceType']

                if instance_state == 'running':
                    analysis['running_instances'] += 1
                elif instance_state == 'stopped':
                    analysis['stopped_instances'] += 1

                analysis['instance_types'][instance_type] = \
                    analysis['instance_types'].get(instance_type, 0) + 1

                # Get instance metrics
                metrics = self._get_instance_metrics(instance['InstanceId'])
                
                instance_data = {
                    'id': instance['InstanceId'],
                    'type': instance_type,
                    'state': instance_state,
                    'launch_time': instance.get('LaunchTime', '').isoformat(),
                    'metrics': metrics,
                    'platform': instance.get('Platform', 'linux'),
                    'vpc_id': instance.get('VpcId', ''),
                    'tags': instance.get('Tags', [])
                }

                analysis['instances'].append(instance_data)

                # Check for optimization opportunities
                self._check_optimization_opportunities(instance, metrics, analysis)

        # Add Graviton opportunity if applicable
        self._check_graviton_opportunities(analysis)

        return analysis

    def _get_instance_metrics(self, instance_id, days=7):
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days)

        metrics = {}
        for metric_name in ['CPUUtilization', 'NetworkIn', 'NetworkOut', 'DiskReadOps', 'DiskWriteOps']:
            response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName=metric_name,
                Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
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
        instance_id = instance['InstanceId']

        # Check CPU utilization
        if metrics.get('CPUUtilization', {}).get('average', 0) < 20:
            analysis['optimization_opportunities'].append({
                'instance_id': instance_id,
                'type': 'Low CPU Utilization',
                'description': 'Consider downsizing instance due to low CPU usage',
                'current_value': f"{metrics['CPUUtilization']['average']:.1f}%",
                'estimated_savings': '30%'
            })

        # Check for old generation instances
        instance_type = instance['InstanceType']
        instance_family = instance_type.split('.')[0]
        if instance_family in ['t2', 'm4', 'c4', 'r4']:
            analysis['optimization_opportunities'].append({
                'instance_id': instance_id,
                'type': 'Old Generation Instance',
                'description': f'Consider upgrading {instance_type} to newer generation',
                'current_value': instance_type,
                'estimated_savings': '10-20%'
            })

        # Check for stopped instances
        if instance['State']['Name'] == 'stopped':
            launch_time = instance.get('LaunchTime')
            if launch_time:
                days_stopped = (datetime.now(launch_time.tzinfo) - launch_time).days
                if days_stopped > 30:
                    analysis['optimization_opportunities'].append({
                        'instance_id': instance_id,
                        'type': 'Long-term Stopped Instance',
                        'description': 'Instance stopped for over 30 days',
                        'current_value': f'{days_stopped} days',
                        'estimated_savings': '100%'
                    })

    def _check_graviton_opportunities(self, analysis):
        graviton_eligible_count = 0
        total_eligible_cost = 0

        for instance in analysis['instances']:
            instance_type = instance['type']
            if instance_type.startswith(('t3', 'm5', 'c5', 'r5')):
                graviton_eligible_count += 1
                # Rough estimation of instance cost
                total_eligible_cost += analysis['total_cost'] / analysis['total_instances']

        if graviton_eligible_count > 0:
            estimated_savings = total_eligible_cost * 0.2  # Assuming 20% cost reduction
            analysis['optimization_opportunities'].append({
                'type': 'Graviton Migration Opportunity',
                'description': f'{graviton_eligible_count} instances eligible for Graviton migration',
                'current_value': f'{graviton_eligible_count} instances',
                'estimated_savings': f'${estimated_savings:.2f}'
            })