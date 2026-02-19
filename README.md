## Setup

### conda

#### environment.yml
```bash
conda env create -f environment.yml
```

#### from scratch
```bash
conda create -n partior
```

## Running Vault Locally
docker run -d --name vault-dev -p 8200:8200 -e VAULT_DEV_ROOT_TOKEN_ID=myroot hashicorp/vault:latest

## Set environment variables so we can talk to Vault
export VAULT_ADDR="http://localhost:8200"
export VAULT_TOKEN="myroot"

## Store a secret
docker exec -e VAULT_ADDR="http://127.0.0.1:8200" -e VAULT_TOKEN='myroot' vault-dev vault kv put secret/myapp/config db_password="SuperSecretPassword123" api_key="ABC-XYZ-789"

## Retreieve a secret
docker exec -e VAULT_ADDR='http://127.0.0.1:8200' -e VAULT_TOKEN='myroot' vault-dev vault kv get secret/myapp/config

## Create structure
```bash
mkdir -p app tests vault/certs
touch app/__init__.py
touch app/main.py
touch app/vault_client.py
touch tests/test_vault_integration.py
touch .env
```

## Files

### app/vault_client.py
Handles all communication with Vault

### app/main.py
Creates a simple web API with endpoints

## Run tests locally
```bash
python -m pytest tests/ -v
```