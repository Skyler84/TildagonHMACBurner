from functools import wraps
from flask import jsonify, request, g
import os
from datetime import datetime

from ..db import get_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Missing API token'}), 401
        
        # Handle "Bearer <token>" format
        if token.startswith('Bearer '):
            token = token[7:]
        
        token_data = get_token(token)
        if not token_data:
            return jsonify({'message': 'Invalid API token'}), 401

        g.token_data = token_data
        
        return f(*args, **kwargs)
    return decorated
