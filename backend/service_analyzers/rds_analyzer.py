import boto3
import os

class RDSAnalyzer:
    def __init__(self):
        self.rds = boto3.client('rds',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION', 'us-east-1')
        )

    def analyze(self):
        instances = self.rds.describe_db_instances()
        analysis = {
            'total_instances': 0,
            'engine_types': {},
            'instances': []
        }

        for instance in instances['DBInstances']:
            analysis['total_instances'] += 1
            engine = instance['Engine']
            analysis['engine_types'][engine] = \
                analysis['engine_types'].get(engine, 0) + 1

            instance_data = {
                'identifier': instance['DBInstanceIdentifier'],
                'engine': engine,
                'status': instance['DBInstanceStatus'],
                'size': instance['DBInstanceClass']
            }
            analysis['instances'].append(instance_data)

        return analysis