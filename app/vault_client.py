"""
Vault Client - Handles secure communication with HashiCorp Vault
"""
import hvac
import os
from typing import Optional, Dict

class VaultClient:
    """Client for interacting with HashiCorp Vault"""
    
    def __init__(self, vault_url: str, vault_token: str):
        """
        Initialize Vault client
        
        Args:
            vault_url: URL of Vault server (e.g., http://localhost:8200)
            vault_token: Authentication token for Vault
        """
        self.client = hvac.Client(url=vault_url, token=vault_token)
        
        # Verify we can connect
        if not self.client.is_authenticated():
            raise Exception("Failed to authenticate with Vault")
        
        print(f"✓ Successfully connected to Vault at {vault_url}")
    
    def get_secret(self, path: str) -> Optional[Dict]:
        """
        Retrieve a secret from Vault
        
        Args:
            path: Path to the secret (e.g., 'secret/myapp/config')
        
        Returns:
            Dictionary containing the secret data, or None if not found
        """
        try:
            # Read secret from Vault
            response = self.client.secrets.kv.v2.read_secret_version(
                path=path,
                mount_point='secret',
                raise_on_deleted_version=False  # Added this line
            )
            
            # Extract the actual secret data
            secret_data = response['data']['data']
            print(f"✓ Successfully retrieved secret from {path}")
            return secret_data
            
        except Exception as e:
            print(f"✗ Failed to retrieve secret: {str(e)}")
            return None
    
    def create_secret(self, path: str, secret_data: Dict) -> bool:
        """
        Store a secret in Vault
        
        Args:
            path: Path where to store the secret
            secret_data: Dictionary of key-value pairs to store
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret=secret_data,
                mount_point='secret'
            )
            print(f"✓ Successfully stored secret at {path}")
            return True
            
        except Exception as e:
            print(f"✗ Failed to store secret: {str(e)}")
            return False