import boto3
from datetime import datetime, timedelta
import os

class CostOptimizer:
    def __init__(self):
        self.ce = boto3.client('ce',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION', 'us-east-1')
        )

    def get_recommendations(self):
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

        recommendations = self.ce.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='MONTHLY',
            Metrics=['BlendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        )

        return self._process_recommendations(recommendations)

    def get_savings_overview(self):
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

        response = self.ce.get_savings_plans_utilization_details(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            }
        )

        return self._process_savings_overview(response)

    def _process_recommendations(self, data):
        recommendations = []
        for result in data['ResultsByTime']:
            for group in result['Groups']:
                service = group['Keys'][0]
                cost = float(group['Metrics']['BlendedCost']['Amount'])
                if cost > 100:  # Example threshold
                    recommendations.append({
                        'title': f'High {service} Usage',
                        'description': f'Consider reviewing {service} usage patterns',
                        'potentialSavings': round(cost * 0.2, 2)  # Example 20% saving
                    })
        return recommendations

    def _process_savings_overview(self, data):
        total_savings = 0
        for utilization in data.get('SavingsPlansUtilizationDetails', []):
            total_savings += float(utilization.get('Savings', {}).get('Amount', 0))

        return {
            'total_savings': round(total_savings, 2),
            'recommendations': self.get_recommendations()
        }