# DevSecOps Pipeline Demo

A demonstration of security-integrated CI/CD pipeline featuring HashiCorp Vault secret management, automated security scanning, and containerized deployment.

## 🎯 Overview

This project demonstrates core DevSecOps practices by integrating security at every stage of the development lifecycle:

- **Secret Management**: HashiCorp Vault for secure credential storage
- **Automated Testing**: Integration tests validating Vault connectivity
- **Security Scanning**: Multi-layer vulnerability detection
- **Containerization**: Docker for consistent deployments
- **CI/CD Pipeline**: GitHub Actions automating the entire workflow

## 🏗️ Architecture

```
┌─────────────┐
│   GitHub    │
│  Repository │
└──────┬──────┘
       │ Push/PR
       ▼
┌─────────────────────────────────────────┐
│       GitHub Actions CI Pipeline        │
├─────────────────────────────────────────┤
│  1. Checkout Code                       │
│  2. Setup Python Environment            │
│  3. Install Dependencies                │
│  4. Start HashiCorp Vault               │
│  5. Run Flask Application               │
│  6. Execute Integration Tests           │
│  7. Security Scanning:                  │
│     - pip-audit (Dependencies)          │
│     - Bandit (SAST)                     │
│     - Trivy (Container)                 │
│  8. Build Docker Image                  │
│  9. Generate Security Reports           │
└─────────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│  Artifacts  │
│  & Reports  │
└─────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Docker
- Git

### Local Setup

```bash
# Clone repository
git clone <your-repo-url>
cd partior-devsecops

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Vault in development mode
docker run -d --name vault-dev -p 8200:8200 \
  -e VAULT_DEV_ROOT_TOKEN_ID=myroot \
  hashicorp/vault:latest

# Set environment variables
export VAULT_ADDR="http://localhost:8200"
export VAULT_TOKEN="myroot"

# Store test secret
docker exec -e VAULT_ADDR="http://127.0.0.1:8200" -e VAULT_TOKEN='myroot' \
  vault-dev vault kv put secret/myapp/config \
  db_password="SuperSecretPassword123" \
  api_key="ABC-XYZ-789"

# Run the application
python -m app.main
```

### Run Tests

```bash
# Ensure Flask is running in another terminal
python -m pytest tests/ -v
```

## 🔒 Security Features

### 1. Secret Management
- **Tool**: HashiCorp Vault
- **Purpose**: Securely store and retrieve sensitive credentials
- **Implementation**: KV v2 secrets engine with token authentication

### 2. Dependency Scanning
- **Tool**: pip-audit
- **Scans**: Python package dependencies
- **Detects**: Known CVEs in libraries

### 3. Static Application Security Testing (SAST)
- **Tool**: Bandit
- **Scans**: Python source code
- **Detects**: Security anti-patterns, hardcoded secrets, insecure functions

### 4. Container Vulnerability Scanning
- **Tool**: Trivy
- **Scans**: Docker images
- **Detects**: OS and application-level vulnerabilities

## 📁 Project Structure

```
partior-devsecops/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions workflow
├── app/
│   ├── __init__.py
│   ├── main.py                 # Flask application
│   └── vault_client.py         # Vault integration
├── tests/
│   └── test_vault_integration.py  # Integration tests
├── vault/
│   └── certs/                  # TLS certificates (future)
├── Dockerfile                  # Container image definition
├── requirements.txt            # Python dependencies
├── .env                        # Local environment variables
└── README.md
```

## 🔧 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Application | Python 3.13, Flask | REST API |
| Secret Management | HashiCorp Vault | Secure credential storage |
| CI/CD | GitHub Actions | Automation pipeline |
| Testing | pytest | Integration testing |
| Containerization | Docker | Application packaging |
| Security Scanning | pip-audit, Bandit, Trivy | Vulnerability detection |

## 🎭 Demo Endpoints

### Health Check
```bash
curl http://localhost:5000/
```

### Retrieve Secret (Demo Only)
```bash
curl http://localhost:5000/get-secret
```

### Detailed Health
```bash
curl http://localhost:5000/health
```

## 📊 CI/CD Pipeline

The GitHub Actions pipeline automatically:
1. Sets up the environment
2. Deploys HashiCorp Vault
3. Runs integration tests
4. Performs security scans
5. Builds Docker image
6. Generates security reports

View pipeline status: `https://github.com/Nightey3s/partior-devsecops/actions`

## 🔐 Security Scan Results

Latest scan results are available as downloadable artifacts from each GitHub Actions run.

### Sample Results
- **pip-audit**: ✅ 0 vulnerable dependencies
- **Bandit**: ✅ All high-severity issues resolved
- **Trivy**: ✅ Container scan completed

## 🚧 Future Enhancements

- [ ] TLS/SSL for Vault production deployment
- [ ] Helm charts for Kubernetes deployment
- [ ] Dynamic secrets generation
- [ ] Vault authentication via Kubernetes service accounts
- [ ] DAST (Dynamic Application Security Testing)
- [ ] Infrastructure as Code with Terraform

## 📝 Key Learnings

This project demonstrates:
- Integration of security tools into CI/CD pipelines
- Secret management best practices
- Automated security scanning workflows
- Container security considerations
- DevSecOps culture and practices

## 👤 Author

Brian Tham  
Singapore Institute of Technology  
Applied Artificial Intelligence

---

**Note**: This is a demonstration project for educational purposes. Production deployments would require additional hardening, authentication mechanisms, and monitoring solutions.