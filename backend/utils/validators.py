from datetime import datetime
from typing import Tuple, Optional
from functools import wraps
from flask import request, jsonify

def validate_date_format(date_str: str) -> Tuple[bool, Optional[str]]:
    """Validate date string format"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True, None
    except ValueError:
        return False, 'Date must be in YYYY-MM-DD format'

def validate_date_range(start_date: str, end_date: str) -> Tuple[bool, Optional[str]]:
    """Validate date range"""
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        if end < start:
            return False, 'End date must be after start date'
            
        if (end - start).days > 365:
            return False, 'Date range cannot exceed 365 days'
            
        return True, None
    except ValueError:
        return False, 'Invalid date format'

def require_params(*params):
    """Decorator to validate required request parameters"""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            missing = [p for p in params if p not in request.args]
            if missing:
                return jsonify({
                    'error': f'Missing required parameters: {", ".join(missing)}'
                }), 400
            return f(*args, **kwargs)
        return wrapped
    return decorator

def validate_aws_account(account_id: str) -> Tuple[bool, Optional[str]]:
    """Validate AWS account ID format"""
    if not account_id.isdigit() or len(account_id) != 12:
        return False, 'Invalid AWS account ID format'
    return True, None