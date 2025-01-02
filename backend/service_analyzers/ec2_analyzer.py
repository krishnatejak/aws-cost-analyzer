import boto3
import os

class EC2Analyzer:
    def __init__(self):
        self.ec2 = boto3.client('ec2',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION', 'us-east-1')
        )
        self.cloudwatch = boto3.client('cloudwatch')

    def analyze(self):
        instances = self.ec2.describe_instances()
        analysis = {
            'total_instances': 0,
            'running_instances': 0,
            'stopped_instances': 0,
            'instance_types': {},
            'instances': []
        }

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

                instance_data = {
                    'id': instance['InstanceId'],
                    'type': instance_type,
                    'state': instance_state,
                    'launch_time': instance.get('LaunchTime', '').isoformat()
                }
                analysis['instances'].append(instance_data)

        return analysis