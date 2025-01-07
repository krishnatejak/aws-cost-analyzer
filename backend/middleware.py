from functools import wraps
from flask import request, jsonify
import jwt
from config import Config

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(*args, **kwargs)
    return decorated