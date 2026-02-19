"""
Main Flask Application - Demonstrates secure secret retrieval
"""
from flask import Flask, jsonify
import os
from app.vault_client import VaultClient

app = Flask(__name__)

# Initialize Vault client
# In production, these would come from secure environment variables
VAULT_URL = os.getenv('VAULT_ADDR', 'http://localhost:8200')
VAULT_TOKEN = os.getenv('VAULT_TOKEN', 'myroot')

try:
    vault = VaultClient(VAULT_URL, VAULT_TOKEN)
except Exception as e:
    print(f"Failed to initialize Vault client: {e}")
    vault = None

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "devsecops-demo",
        "vault_connected": vault is not None
    })

@app.route('/get-secret')
def get_secret():
    """
    Retrieve secret from Vault
    
    Returns:
        JSON response with secret data or error message
    """
    if vault is None:
        return jsonify({
            "error": "Vault client not initialized"
        }), 500
    
    # Retrieve the secret we stored earlier
    secret_data = vault.get_secret('myapp/config')
    
    if secret_data:
        # In production, you wouldn't return secrets directly!
        # This is just for demonstration
        return jsonify({
            "success": True,
            "message": "Secret retrieved successfully",
            "data": {
                "db_password_length": len(secret_data.get('db_password', '')),
                "api_key_present": 'api_key' in secret_data,
                # Show first 3 chars only for demo
                "api_key_preview": secret_data.get('api_key', '')[:3] + '...'
            }
        })
    else:
        return jsonify({
            "success": False,
            "error": "Failed to retrieve secret"
        }), 500

@app.route('/health')
def health():
    """Detailed health check"""
    vault_healthy = False
    
    if vault:
        try:
            # Try to read a secret to verify connection
            vault.client.is_authenticated()
            vault_healthy = True
        except:
            pass
    
    return jsonify({
        "api": "healthy",
        "vault": "connected" if vault_healthy else "disconnected"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)