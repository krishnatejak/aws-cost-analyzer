from typing import Dict, List
import boto3

class S3Analyzer:
    def __init__(self):
        self.s3 = boto3.client('s3')

    def analyze_buckets(self) -> Dict:
        buckets = self._get_all_buckets()
        return {
            'total_buckets': len(buckets),
            'bucket_details': self._get_bucket_details(buckets),
            'recommendations': self._generate_recommendations(buckets)
        }

    def _get_all_buckets(self) -> List:
        response = self.s3.list_buckets()
        return response['Buckets']

    def _get_bucket_details(self, buckets: List) -> List:
        details = []
        for bucket in buckets:
            try:
                lifecycle = self.s3.get_bucket_lifecycle_configuration(Bucket=bucket['Name'])
            except:
                lifecycle = None

            details.append({
                'name': bucket['Name'],
                'creation_date': bucket['CreationDate'].isoformat(),
                'has_lifecycle': lifecycle is not None,
                'size': self._get_bucket_size(bucket['Name'])
            })
        return details

    def _get_bucket_size(self, bucket_name: str) -> int:
        total_size = 0
        paginator = self.s3.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket_name):
            if 'Contents' in page:
                for obj in page['Contents']:
                    total_size += obj['Size']
        return total_size

    def _generate_recommendations(self, buckets: List) -> List:
        recommendations = []
        for bucket in buckets:
            try:
                versioning = self.s3.get_bucket_versioning(Bucket=bucket['Name'])
                if 'Status' not in versioning:
                    recommendations.append({
                        'bucket_name': bucket['Name'],
                        'type': 'enable_versioning',
                        'message': f'Consider enabling versioning for bucket {bucket["Name"]} for data protection'
                    })
            except:
                pass
        return recommendations