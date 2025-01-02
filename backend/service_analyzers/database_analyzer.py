import boto3
from datetime import datetime, timedelta
from typing import Dict, List

class DatabaseAnalyzer:
    def __init__(self):
        self.rds = boto3.client('rds')
        self.dynamodb = boto3.client('dynamodb')
        self.cloudwatch = boto3.client('cloudwatch')

    def analyze_all_databases(self) -> Dict:
        """Analyze all database services"""
        return {
            'rds': self.analyze_rds(),
            'dynamodb': self.analyze_dynamodb(),
            'recommendations': self._generate_recommendations()
        }

    def analyze_rds(self) -> Dict:
        """Analyze RDS instances and clusters"""
        instances = self.rds.describe_db_instances()
        clusters = self.rds.describe_db_clusters()

        analysis = {
            'instances': self._analyze_rds_instances(instances['DBInstances']),
            'clusters': self._analyze_rds_clusters(clusters['DBClusters']),
            'metrics': self._get_rds_metrics(),
            'costs': self._analyze_rds_costs()
        }

        return analysis

    def analyze_dynamodb(self) -> Dict:
        """Analyze DynamoDB tables"""
        tables = self.dynamodb.list_tables()
        
        analysis = {
            'tables': self._analyze_dynamodb_tables(tables['TableNames']),
            'metrics': self._get_dynamodb_metrics(),
            'costs': self._analyze_dynamodb_costs()
        }

        return analysis

    def _analyze_rds_instances(self, instances: List[Dict]) -> List[Dict]:
        """Analyze individual RDS instances"""
        instance_analysis = []
        
        for instance in instances:
            metrics = self._get_instance_metrics(instance['DBInstanceIdentifier'])
            
            analysis = {
                'identifier': instance['DBInstanceIdentifier'],
                'instance_class': instance['DBInstanceClass'],
                'engine': instance['Engine'],
                'storage': {
                    'allocated': instance['AllocatedStorage'],
                    'used': self._get_storage_used(instance['DBInstanceIdentifier']),
                    'type': instance['StorageType']
                },
                'performance': {
                    'cpu_utilization': metrics['cpu'],
                    'memory_utilization': metrics['memory'],
                    'iops': metrics['iops']
                },
                'multi_az': instance.get('MultiAZ', False),
                'optimization_opportunities': self._identify_instance_optimizations(instance, metrics)
            }
            
            instance_analysis.append(analysis)

        return instance_analysis

    def _get_instance_metrics(self, instance_id: str) -> Dict:
        """Get detailed metrics for an RDS instance"""
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=14)

        metrics = {
            'cpu': self._get_metric_statistics(
                'AWS/RDS', 'CPUUtilization',
                [{'Name': 'DBInstanceIdentifier', 'Value': instance_id}],
                start_time, end_time
            ),
            'memory': self._get_metric_statistics(
                'AWS/RDS', 'FreeableMemory',
                [{'Name': 'DBInstanceIdentifier', 'Value': instance_id}],
                start_time, end_time
            ),
            'iops': self._get_metric_statistics(
                'AWS/RDS', 'ReadIOPS',
                [{'Name': 'DBInstanceIdentifier', 'Value': instance_id}],
                start_time, end_time
            )
        }

        return metrics

    def _analyze_dynamodb_tables(self, table_names: List[str]) -> List[Dict]:
        """Analyze DynamoDB tables"""
        table_analysis = []

        for table_name in table_names:
            table = self.dynamodb.describe_table(TableName=table_name)['Table']
            metrics = self._get_dynamodb_table_metrics(table_name)

            analysis = {
                'table_name': table_name,
                'size_bytes': table['TableSizeBytes'],
                'item_count': table['ItemCount'],
                'provisioned_capacity': {
                    'read': table.get('ProvisionedThroughput', {}).get('ReadCapacityUnits', 0),
                    'write': table.get('ProvisionedThroughput', {}).get('WriteCapacityUnits', 0)
                },
                'performance': {
                    'consumed_read_capacity': metrics['read_capacity'],
                    'consumed_write_capacity': metrics['write_capacity'],
                    'throttled_requests': metrics['throttled_requests']
                },
                'optimization_opportunities': self._identify_table_optimizations(table, metrics)
            }

            table_analysis.append(analysis)

        return table_analysis

    def _get_dynamodb_table_metrics(self, table_name: str) -> Dict:
        """Get metrics for a DynamoDB table"""
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=14)

        metrics = {
            'read_capacity': self._get_metric_statistics(
                'AWS/DynamoDB', 'ConsumedReadCapacityUnits',
                [{'Name': 'TableName', 'Value': table_name}],
                start_time, end_time
            ),
            'write_capacity': self._get_metric_statistics(
                'AWS/DynamoDB', 'ConsumedWriteCapacityUnits',
                [{'Name': 'TableName', 'Value': table_name}],
                start_time, end_time
            ),
            'throttled_requests': self._get_metric_statistics(
                'AWS/DynamoDB', 'ThrottledRequests',
                [{'Name': 'TableName', 'Value': table_name}],
                start_time, end_time
            )
        }

        return metrics

    def _get_metric_statistics(self, namespace: str, metric_name: str, 
                             dimensions: List[Dict], start_time: datetime, 
                             end_time: datetime) -> List[Dict]:
        """Get CloudWatch metric statistics"""
        response = self.cloudwatch.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=dimensions,
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,
            Statistics=['Average', 'Maximum', 'Minimum', 'Sum']
        )
        return response['Datapoints']

    def _identify_instance_optimizations(self, instance: Dict, metrics: Dict) -> List[Dict]:
        """Identify optimization opportunities for RDS instance"""
        optimizations = []

        # Check for underutilized instances
        avg_cpu = sum(m['Average'] for m in metrics['cpu']) / len(metrics['cpu']) if metrics['cpu'] else 0
        if avg_cpu < 40:
            optimizations.append({
                'type': 'instance_sizing',
                'description': 'Instance is underutilized',
                'recommendation': 'Consider downsizing instance class',
                'potential_savings': '20-40%'
            })

        # Check for Aurora migration opportunity
        if instance['Engine'] in ['mysql', 'postgres']:
            optimizations.append({
                'type': 'modernization',
                'description': 'Compatible with Aurora',
                'recommendation': 'Evaluate Aurora migration',
                'potential_savings': '10-30%'
            })

        return optimizations

    def _identify_table_optimizations(self, table: Dict, metrics: Dict) -> List[Dict]:
        """Identify optimization opportunities for DynamoDB table"""
        optimizations = []

        # Check for over-provisioning
        provisioned_read = table.get('ProvisionedThroughput', {}).get('ReadCapacityUnits', 0)
        provisioned_write = table.get('ProvisionedThroughput', {}).get('WriteCapacityUnits', 0)
        
        avg_read = sum(m['Average'] for m in metrics['read_capacity']) / len(metrics['read_capacity']) if metrics['read_capacity'] else 0
        avg_write = sum(m['Average'] for m in metrics['write_capacity']) / len(metrics['write_capacity']) if metrics['write_capacity'] else 0

        if provisioned_read > 0 and (avg_read / provisioned_read) < 0.4:
            optimizations.append({
                'type': 'capacity_optimization',
                'description': 'Read capacity is over-provisioned',
                'recommendation': 'Reduce read capacity or switch to on-demand',
                'potential_savings': '30-50%'
            })

        if provisioned_write > 0 and (avg_write / provisioned_write) < 0.4:
            optimizations.append({
                'type': 'capacity_optimization',
                'description': 'Write capacity is over-provisioned',
                'recommendation': 'Reduce write capacity or switch to on-demand',
                'potential_savings': '30-50%'
            })

        return optimizations