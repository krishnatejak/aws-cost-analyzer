import boto3
from typing import Dict, List
from datetime import datetime, timedelta

class RDSAnalyzer:
    def __init__(self):
        self.rds = boto3.client('rds')
        self.cloudwatch = boto3.client('cloudwatch')
        
    def analyze_instance_types(self) -> Dict:
        """Analyze RDS instance types and potential optimizations"""
        instances = self.rds.describe_db_instances()
        analysis = {}
        
        for instance in instances['DBInstances']:
            instance_id = instance['DBInstanceIdentifier']
            analysis[instance_id] = {
                'instance_class': instance['DBInstanceClass'],
                'engine': instance['Engine'],
                'storage': instance['AllocatedStorage'],
                'multi_az': instance.get('MultiAZ', False),
                'metrics': self._get_instance_metrics(instance_id),
                'recommendations': self._generate_instance_recommendations(instance)
            }
        
        return analysis
    
    def _get_instance_metrics(self, instance_id: str) -> Dict:
        """Get detailed RDS instance metrics"""
        metrics = {}
        
        # CPU Utilization
        cpu = self.cloudwatch.get_metric_statistics(
            Namespace='AWS/RDS',
            MetricName='CPUUtilization',
            Dimensions=[{'Name': 'DBInstanceIdentifier', 'Value': instance_id}],
            StartTime=datetime.utcnow() - timedelta(days=14),
            EndTime=datetime.utcnow(),
            Period=3600,
            Statistics=['Average', 'Maximum']
        )
        
        # Memory Usage
        memory = self.cloudwatch.get_metric_statistics(
            Namespace='AWS/RDS',
            MetricName='FreeableMemory',
            Dimensions=[{'Name': 'DBInstanceIdentifier', 'Value': instance_id}],
            StartTime=datetime.utcnow() - timedelta(days=14),
            EndTime=datetime.utcnow(),
            Period=3600,
            Statistics=['Average', 'Minimum']
        )
        
        # IOPS Usage
        iops = self.cloudwatch.get_metric_statistics(
            Namespace='AWS/RDS',
            MetricName='ReadIOPS',
            Dimensions=[{'Name': 'DBInstanceIdentifier', 'Value': instance_id}],
            StartTime=datetime.utcnow() - timedelta(days=14),
            EndTime=datetime.utcnow(),
            Period=3600,
            Statistics=['Sum']
        )
        
        metrics['cpu'] = cpu['Datapoints']
        metrics['memory'] = memory['Datapoints']
        metrics['iops'] = iops['Datapoints']
        
        return metrics
    
    def _generate_instance_recommendations(self, instance: Dict) -> List[Dict]:
        """Generate specific recommendations for an RDS instance"""
        recommendations = []
        
        # Check Aurora Serverless v2 compatibility
        if self._is_aurora_serverless_compatible(instance):
            recommendations.append({
                'type': 'modernization',
                'title': 'Consider Aurora Serverless v2',
                'description': 'Instance workload pattern suggests good fit for Aurora Serverless v2',
                'potential_savings': '30-50%',
                'effort': 'Medium',
                'steps': [
                    'Export current database schema and data',
                    'Create Aurora Serverless v2 cluster',
                    'Import data and verify',
                    'Update application connection strings',
                    'Monitor performance and costs'
                ]
            })
        
        # Check for oversized instances
        if self._is_oversized(instance):
            recommendations.append({
                'type': 'rightsizing',
                'title': 'Instance Rightsizing Opportunity',
                'description': 'Current instance shows consistent low resource utilization',
                'potential_savings': '20-40%',
                'effort': 'Low',
                'steps': [
                    'Review current utilization metrics',
                    'Select appropriate instance size',
                    'Schedule modification window',
                    'Monitor performance post-change'
                ]
            })
        
        return recommendations
    
    def _is_aurora_serverless_compatible(self, instance: Dict) -> bool:
        """Check if instance is compatible with Aurora Serverless v2"""
        compatible_engines = ['aurora-mysql', 'aurora-postgresql']
        return instance['Engine'] in compatible_engines
    
    def _is_oversized(self, instance: Dict) -> bool:
        """Check if instance is potentially oversized"""
        instance_id = instance['DBInstanceIdentifier']
        metrics = self._get_instance_metrics(instance_id)
        
        # Calculate average CPU utilization
        if metrics['cpu']:
            avg_cpu = sum(dp['Average'] for dp in metrics['cpu']) / len(metrics['cpu'])
            return avg_cpu < 40  # Less than 40% CPU utilization suggests oversizing
        
        return False