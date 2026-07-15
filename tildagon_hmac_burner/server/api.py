import os
from flask import jsonify, request
from .app import app
from .auth.token import token_required
from ..common.master_secret import check_master_secret
from ..common.hmac_key import generate_hmac_key



# API token from environment variable
API_TOKEN = os.getenv('API_TOKEN')
MASTER_SECRET = os.getenv('MASTER_SECRET')
check_master_secret(MASTER_SECRET)  # Validate the master secret if provided


@app.route('/api/status', methods=['GET'])
@token_required
def status():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Server is running'}), 200


@app.route('/api/data', methods=['POST'])
@token_required
def post_data():
    """Accept POST data"""
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    return jsonify({'message': 'Data received', 'data': data}), 201


@app.route('/api/data', methods=['GET'])
@token_required
def get_data():
    """Retrieve data"""
    return jsonify({'message': 'Sample data', 'data': {'id': 1, 'name': 'example'}}), 200

@app.route('/api/generate_badge_secret/', methods=['POST'])
@token_required
def generate_badge_secret():
    """
    Endpoint to generate a combined secret based on the provided MAC address.
    Expects JSON payload with 'mac' field.
    """
    data = request.get_json()
    if not data or 'mac' not in data:
        return jsonify({'message': 'MAC address is required'}), 400
    
    mac_str = data['mac']
    try:
        hmac_key = generate_hmac_key(MASTER_SECRET, mac_str)
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    
    return jsonify({'hmac_key': hmac_key.hex()}), 200
