from flask import Blueprint, request, jsonify
import jwt
from datetime import datetime, timedelta
from config import Config

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Could not verify'}), 401
    
    # Add your user verification logic here
    # For demo, using basic check
    if auth.username == 'admin' and auth.password == 'password':
        token = jwt.encode({
            'user': auth.username,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, Config.SECRET_KEY)
        return jsonify({'token': token})
    
    return jsonify({'message': 'Could not verify'}), 401