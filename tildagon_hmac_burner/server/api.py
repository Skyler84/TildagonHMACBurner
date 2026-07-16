import os
from flask import jsonify, request, g
from .app import app
from .auth.token import token_required
from ..common.master_secret import check_master_secret
from ..common.hmac_key import generate_hmac_key
from .db import record_hmac_request


# API token from environment variable
API_TOKEN = os.getenv('API_TOKEN')
MASTER_SECRET = os.getenv('MASTER_SECRET')
check_master_secret(MASTER_SECRET)  # Validate the master secret if provided

@app.route('/api/status', methods=['GET'])
@token_required
def status():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Server is running'}), 200

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

    print("Generated badge secret for MAC:", mac_str)

    record_hmac_request(mac_str, g.token_data["id"])
    
    return jsonify({'hmac_key': hmac_key.hex()}), 200
