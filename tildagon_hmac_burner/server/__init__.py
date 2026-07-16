import os
from flask import Flask, jsonify, request
from .app import app
from .api import *

from .db import init_db

# Initialize the token database
init_db()

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'message': 'Internal server error'}), 500

