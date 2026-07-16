import sqlite3
import os

DB_PATH = os.environ.get('TOKEN_DB_PATH', 'tildagon_hmac_burner.db')

def init_db():
    """Initialize the database."""
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
    c.execute('''
        CREATE TABLE IF NOT EXISTS generated_hmacs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mac TEXT NOT NULL,
            issued_for INTEGER REFERENCES tokens(id) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def open_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_token(token, permissions=None):
    """Create a new token in the database."""
    if permissions is None:
        permissions = '[]'
    conn = open_conn()
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

def update_permissions(token, permissions):
    """Update permissions for a token."""
    conn = open_conn()
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
    conn = open_conn()
    c = conn.cursor()
    c.execute('SELECT id, token, permissions, created_at FROM tokens WHERE token = ?', (token,))
    row = c.fetchone()
    conn.close()
    return row

def delete_token(token):
    """Delete a token from the database."""
    conn = open_conn()
    c = conn.cursor()
    c.execute('DELETE FROM tokens WHERE token = ?', (token,))
    conn.commit()
    deleted = c.rowcount > 0
    conn.close()
    return deleted

def record_hmac_request(mac, token_id):
    """Records that a token requested a HMAC."""
    conn = open_conn()
    c = conn.cursor()
    c.execute('INSERT INTO generated_hmacs (mac, issued_for) values (?, ?)', (mac, token_id))
    conn.commit()
    conn.close()
