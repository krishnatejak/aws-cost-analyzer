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
        self.compute_optimizer = boto3.client('compute-optimizer')

    def get_recommendations(self):
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

        recommendations = []

        # Get service cost data
        cost_data = self.ce.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='MONTHLY',
            Metrics=['BlendedCost', 'UsageQuantity'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        )

        # Get compute optimizer recommendations
        try:
            ec2_recommendations = self.compute_optimizer.get_ec2_instance_recommendations()
            recommendations.extend(self._process_ec2_recommendations(ec2_recommendations))
        except Exception as e:
            print(f"Error getting compute optimizer recommendations: {str(e)}")

        # Process cost data for recommendations
        service_recommendations = self._process_cost_recommendations(cost_data)
        recommendations.extend(service_recommendations)

        # Get RI/SP recommendations
        try:
            ri_recommendations = self.ce.get_reservation_purchase_recommendation(
                LookbackPeriodInDays=30,
                TermInYears=1,
                PaymentOption='NO_UPFRONT'
            )
            recommendations.extend(self._process_ri_recommendations(ri_recommendations))
        except Exception as e:
            print(f"Error getting RI recommendations: {str(e)}")

        return recommendations

    def get_savings_overview(self):
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

        # Get Savings Plans utilization
        sp_utilization = self.ce.get_savings_plans_utilization_details(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            }
        )

        # Get Reserved Instance utilization
        ri_utilization = self.ce.get_reservation_utilization(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            }
        )

        return self._process_savings_overview(sp_utilization, ri_utilization)

    def _process_cost_recommendations(self, cost_data):
        recommendations = []
        for result in cost_data['ResultsByTime']:
            for group in result['Groups']:
                service = group['Keys'][0]
                cost = float(group['Metrics']['BlendedCost']['Amount'])
                usage = float(group['Metrics']['UsageQuantity']['Amount'])

                if cost > 100:  # Cost threshold
                    if usage == 0:
                        recommendations.append({
                            'title': f'Unused {service} Resources',
                            'description': f'Consider removing unused {service} resources',
                            'potentialSavings': round(cost, 2)
                        })
                    elif cost > 1000:  # High cost threshold
                        recommendations.append({
                            'title': f'High {service} Costs',
                            'description': f'Review {service} usage patterns for optimization',
                            'potentialSavings': round(cost * 0.2, 2)  # Estimated 20% savings
                        })

        return recommendations

    def _process_ec2_recommendations(self, recommendations):
        processed = []
        for rec in recommendations.get('instanceRecommendations', []):
            current_instance = rec['currentInstanceType']
            recommended_instance = rec['recommendationOptions'][0]['instanceType']
            
            if current_instance != recommended_instance:
                savings = rec['recommendationOptions'][0]['estimatedMonthlySavings']['value']
                processed.append({
                    'title': 'EC2 Instance Right-sizing',
                    'description': f'Resize {rec['instanceId']} from {current_instance} to {recommended_instance}',
                    'potentialSavings': round(float(savings), 2)
                })

        return processed

    def _process_ri_recommendations(self, recommendations):
        processed = []
        for rec in recommendations.get('Recommendations', []):
            for detail in rec['RecommendationDetails']:
                savings = detail['EstimatedMonthlySavings']
                instance_type = detail['InstanceDetails']['EC2InstanceDetails']['InstanceType']
                processed.append({
                    'title': 'Reserved Instance Opportunity',
                    'description': f'Purchase RI for {instance_type}',
                    'potentialSavings': round(float(savings), 2)
                })

        return processed

    def _process_savings_overview(self, sp_data, ri_data):
        total_savings = 0
        potential_savings = 0

        # Calculate Savings Plans savings
        for utilization in sp_data.get('SavingsPlansUtilizationDetails', []):
            total_savings += float(utilization.get('Savings', {}).get('Amount', 0))
            potential_savings += float(utilization.get('PotentialSavings', {}).get('Amount', 0))

        # Calculate RI savings
        for utilization in ri_data.get('UtilizationsByTime', []):
            total_savings += float(utilization.get('Total', {}).get('NetSavings', {}).get('Amount', 0))
            potential_savings += float(utilization.get('Total', {}).get('PotentialSavings', {}).get('Amount', 0))

        return {
            'realized_savings': round(total_savings, 2),
            'potential_additional_savings': round(potential_savings, 2),
            'recommendations': self.get_recommendations()
        }