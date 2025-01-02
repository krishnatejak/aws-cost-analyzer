from typing import Dict, List
import boto3

class EC2Analyzer:
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.pricing = boto3.client('pricing')

    def analyze_instances(self) -> Dict:
        instances = self._get_all_instances()
        return {
            'total_instances': len(instances),
            'running_instances': len([i for i in instances if i['State']['Name'] == 'running']),
            'stopped_instances': len([i for i in instances if i['State']['Name'] == 'stopped']),
            'instance_types': self._get_instance_type_distribution(instances),
            'recommendations': self._generate_recommendations(instances)
        }

    def _get_all_instances(self) -> List:
        response = self.ec2.describe_instances()
        instances = []
        for reservation in response['Reservations']:
            instances.extend(reservation['Instances'])
        return instances

    def _get_instance_type_distribution(self, instances: List) -> Dict:
        distribution = {}
        for instance in instances:
            instance_type = instance['InstanceType']
            distribution[instance_type] = distribution.get(instance_type, 0) + 1
        return distribution

    def _generate_recommendations(self, instances: List) -> List:
        recommendations = []
        for instance in instances:
            if instance['State']['Name'] == 'stopped':
                recommendations.append({
                    'instance_id': instance['InstanceId'],
                    'type': 'termination_candidate',
                    'message': f'Instance {instance["InstanceId"]} has been stopped. Consider terminating if not needed.'
                })
            # Add more recommendation logic here
        return recommendations