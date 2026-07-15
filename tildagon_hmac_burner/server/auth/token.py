from functools import wraps
from flask import jsonify, request
import sqlite3
import os
from datetime import datetime

DB_PATH = os.environ.get('TOKEN_DB_PATH', 'tokens.db')

def init_db():
    """Initialize the token database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT UNIQUE NOT NULL,
            permissions TEXT DEFAULT '[]',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def create_token(token, permissions=None):
    """Create a new token in the database."""
    if permissions is None:
        permissions = '[]'
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO tokens (token, permissions)
            VALUES (?, ?)
        ''', (token, permissions))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def delete_token(token):
    """Delete a token from the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM tokens WHERE token = ?', (token,))
    conn.commit()
    deleted = c.rowcount > 0
    conn.close()
    return deleted

def update_permissions(token, permissions):
    """Update permissions for a token."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        UPDATE tokens
        SET permissions = ?, updated_at = CURRENT_TIMESTAMP
        WHERE token = ?
    ''', (permissions, token))
    conn.commit()
    updated = c.rowcount > 0
    conn.close()
    return updated

def get_token(token):
    """Retrieve token details from the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, token, permissions, created_at FROM tokens WHERE token = ?', (token,))
    row = c.fetchone()
    conn.close()
    return row

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
        
        return f(*args, **kwargs)
    return decorated
