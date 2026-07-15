import ssl
import os

from tildagon_hmac_burner.server import app
if __name__ == '__main__':
    # Create self-signed certificate files if they don't exist
    cert_file = 'cert.pem'
    key_file = 'key.pem'
    
    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        print("Generating self-signed certificate...")
        os.system(f'openssl req -x509 -newkey rsa:2048 -nodes -out {cert_file} -keyout {key_file} -days 365 -subj "/CN=localhost"')
    
    # Create SSL context
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(cert_file, key_file)
    
    # Run HTTPS server
    app.run(host='0.0.0.0', port=5000, ssl_context=ssl_context, debug=False)
