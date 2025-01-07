from flask import Blueprint, request, jsonify
import jwt
from datetime import datetime, timedelta
import os

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    print(auth)
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Could not verify'}), 401
    
    if auth.username == 'admin' and auth.password == 'password':
        token = jwt.encode({
            'user': auth.username,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, os.getenv('SECRET_KEY', 'your-secret-key'))
        return jsonify({'token': token})