import boto3
from botocore.exceptions import ClientError
from functools import wraps
from typing import Any, Callable
from .logger import get_logger

logger = get_logger(__name__)

def get_aws_client(service_name: str, region: str = None) -> boto3.client:
    """Get AWS client with proper configuration and retry handling"""
    try:
        return boto3.client(
            service_name,
            region_name=region,
            config=boto3.Config(
                retries=dict(
                    max_attempts=5,
                    mode='adaptive'
                )
            )
        )
    except Exception as e:
        logger.error(f'Error creating AWS client for {service_name}: {str(e)}')
        raise

def handle_aws_error(func: Callable) -> Callable:
    """Decorator to handle AWS API errors"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            logger.error(f'AWS API Error: {error_code} - {error_message}')
            raise
        except Exception as e:
            logger.error(f'Unexpected error in AWS operation: {str(e)}')
            raise
    return wrapper