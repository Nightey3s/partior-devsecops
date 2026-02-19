"""
Integration tests for Vault connectivity and secret retrieval
"""
import pytest
import os
import requests
import time
from app.vault_client import VaultClient

# Test configuration
VAULT_URL = os.getenv('VAULT_ADDR', 'http://localhost:8200')
VAULT_TOKEN = os.getenv('VAULT_TOKEN', 'myroot')
APP_URL = 'http://localhost:5000'

@pytest.fixture(scope='module')
def vault_client():
    """Create a Vault client for tests"""
    client = VaultClient(VAULT_URL, VAULT_TOKEN)
    
    # Set up test data
    test_secret = {
        'db_password': 'TestPassword123',
        'api_key': 'TEST-KEY-789'
    }
    client.create_secret('myapp/config', test_secret)
    
    yield client
    
    # Cleanup after tests (optional)
    # In real scenarios, you might want to clean up test data

def test_vault_connection(vault_client):
    """Test that we can connect to Vault"""
    assert vault_client.client.is_authenticated()

def test_vault_read_secret(vault_client):
    """Test reading a secret from Vault"""
    secret = vault_client.get_secret('myapp/config')
    
    assert secret is not None
    assert 'db_password' in secret
    assert 'api_key' in secret
    assert secret['db_password'] == 'TestPassword123'

def test_vault_write_secret(vault_client):
    """Test writing a new secret to Vault"""
    new_secret = {'test_key': 'test_value'}
    result = vault_client.create_secret('myapp/test', new_secret)
    
    assert result is True
    
    # Verify it was written
    retrieved = vault_client.get_secret('myapp/test')
    assert retrieved['test_key'] == 'test_value'

def test_api_health_endpoint():
    """Test the Flask app health endpoint"""
    response = requests.get(f'{APP_URL}/health')
    
    assert response.status_code == 200
    data = response.json()
    assert data['api'] == 'healthy'
    assert data['vault'] == 'connected'

def test_api_get_secret_endpoint():
    """Test the Flask app secret retrieval endpoint"""
    response = requests.get(f'{APP_URL}/get-secret')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'data' in data