# 🚀 OpsTrack

## DevOps CI/CD & Cloud Deployment Platform

![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?logo=jenkins&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-EC2-FF9900?logo=amazonaws&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5?logo=kubernetes&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-Infrastructure-844FBA?logo=terraform&logoColor=white)
![Ansible](https://img.shields.io/badge/Ansible-Automation-EE0000?logo=ansible&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-E6522C?logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-Observability-F46800?logo=grafana&logoColor=white)

> OpsTrack is a lightweight Task & Incident Management Platform designed as a hands-on application for implementing DevOps practices across the software delivery lifecycle.

The application consists of a React/Vite frontend, FastAPI backend, and PostgreSQL database.

The project focuses on:

- Containerization
- CI/CD automation
- Cloud deployment
- Infrastructure automation
- Kubernetes orchestration
- Helm-based deployment
- Security scanning
- Application testing
- Metrics and monitoring

---

# 🏗️ DevOps Architecture

```text
Developer
    |
    v
  GitHub
    |
    v
Jenkins CI/CD
    |
    +--------------------+
    |                    |
    v                    v
Backend Tests        Docker Build
                         |
                         v
                    Trivy Scan
                         |
                         v
                    Deployment
                    /         \
                   /           \
                  v             v
              AWS EC2       Kubernetes
                  |           + Helm
                  |              |
                  v              v
                Nginx       Application
                  |           Services
            +-----+-----+
            |           |
            v           v
       Frontend      Backend
                        |
                        v
                    PostgreSQL


Backend Metrics
       |
       v
  Prometheus
       |
       v
    Grafana
🎯 What problem does it solve?

Small operations and engineering teams often need to manage tasks, incidents, deployments, and application health while also maintaining a repeatable software delivery process.

OpsTrack combines a small task and incident management application with a practical DevOps workflow covering:

Source control
Automated testing
Containerization
CI/CD
Cloud deployment
Infrastructure validation
Configuration automation
Kubernetes deployment
Helm releases and rollback
Container security scanning
Application metrics
Monitoring

The application is intentionally lightweight so that the DevOps lifecycle can be demonstrated and validated without unnecessary application complexity.

🧩 Application Architecture

OpsTrack consists of three primary application components:

Frontend
React + Vite
    |
    v
Backend
FastAPI
    |
    v
PostgreSQL

The frontend is served using Nginx in the containerized deployment.

The backend provides REST APIs for:

Authentication
Users
Tasks
Incidents
Comments
Dashboard statistics
Health checks
Database health checks
📁 Repository Structure
opstrack/
│
├── backend/
│   ├── app/
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── Dockerfile
│
├── k8s/
│   ├── deployments/
│   ├── services/
│   └── secrets/
│
├── helm/
│   └── opstrack/
│
├── monitoring/
│   ├── prometheus/
│   └── grafana/
│
├── terraform/
│
├── ansible/
│
├── Jenkinsfile
├── docker-compose.yml
├── .env.example
└── README.md
⚙️ DevOps Implementation

OpsTrack was used as a hands-on project to implement and validate DevOps practices across the software delivery lifecycle.

1. 🔄 CI/CD — Jenkins

Jenkins is used to automate the CI/CD workflow.

The pipeline is defined as code using a Jenkinsfile.

Pipeline flow
GitHub
   |
   v
Jenkins
   |
   +--> Backend Tests
   |
   +--> Docker Image Build
   |
   +--> Trivy Security Scan
   |
   +--> Deployment
   |
   +--> Deployment Verification
Implemented CI/CD activities
Jenkins Pipeline as Code
GitHub repository integration using SSH
Automated backend test execution
Docker image builds
Trivy vulnerability scanning
Deployment automation
Deployment verification
Docker Compose deployment workflow
Ansible deployment integration

The pipeline is designed to validate the application before deployment and verify that the deployed services are responding correctly.

🐳 2. Containerization — Docker

OpsTrack is containerized using Docker.

Application containers
Frontend
React/Vite + Nginx

Backend
FastAPI

Database
PostgreSQL

Docker Compose is used to manage the multi-container application.

Implemented Docker features
Backend Docker image
Frontend Docker image
PostgreSQL container
Docker Compose
Internal Docker networking
Container health checks
Service-to-service communication
Nginx-based frontend serving and routing

Example:

docker compose up --build
☁️ 3. Cloud Deployment — AWS EC2

OpsTrack was deployed on an Ubuntu-based AWS EC2 environment.

Deployment stack
AWS EC2
   |
   +-- Ubuntu
   |
   +-- Docker
   |
   +-- Docker Compose
   |
   +-- Jenkins
   |
   +-- Nginx
   |
   +-- OpsTrack

AWS Security Group configuration was used to provide the required network access for the deployment.

The EC2 deployment was used as a hands-on cloud deployment environment for the project.

🏗️ 4. Infrastructure as Code — Terraform

Terraform was used to represent and validate the existing AWS EC2 infrastructure.

Implemented Terraform workflow
Existing AWS EC2
       |
       v
Terraform Configuration
       |
       v
Terraform Import
       |
       v
Terraform Plan / Validation

Implemented activities:

Terraform configuration
Existing EC2 resource import
terraform fmt
terraform validate
terraform plan
Configuration validation

Terraform was used for infrastructure configuration and validation. The EC2 instance was not provisioned from scratch using Terraform.

🤖 5. Configuration Automation — Ansible

Ansible was used for server configuration verification and deployment automation.

Implemented activities include:

Server configuration checks
Docker environment verification
Docker Compose deployment automation
Ansible playbook execution
Jenkins integration

Example workflow:

Jenkins
   |
   v
Ansible
   |
   v
EC2 Server
   |
   v
Docker Compose
   |
   v
OpsTrack
☸️ 6. Kubernetes — Minikube

OpsTrack was also deployed on Kubernetes using Minikube as a hands-on Kubernetes environment.

Kubernetes components implemented
Deployments
Services
Secrets
Liveness probes
Readiness probes
Multiple backend replicas
Application configuration

Example deployment architecture:

Kubernetes
    |
    +-- Frontend Deployment
    |
    +-- Backend Deployment
    |       |
    |       +-- Replica 1
    |       |
    |       +-- Replica 2
    |
    +-- PostgreSQL
    |
    +-- Services
    |
    +-- Secrets

The backend was scaled to multiple replicas and deployment behavior was validated through Kubernetes.

The Kubernetes implementation is a hands-on Minikube environment and is not presented as a production Kubernetes cluster.

⎈ 7. Helm

OpsTrack was packaged and deployed using Helm.

Implemented Helm activities:

Helm chart creation
Helm-based deployment
Helm upgrade
Configuration changes
Release management
Rollback testing
Troubleshooting after a configuration issue

Example workflow:

Helm Chart
    |
    v
Helm Install
    |
    v
Release
    |
    v
Helm Upgrade
    |
    v
Configuration Issue
    |
    v
Helm Rollback
    |
    v
Healthy Release

A rollback scenario was tested to understand release recovery and troubleshooting.

📊 8. Monitoring — Prometheus & Grafana

The FastAPI backend was instrumented to expose application metrics.

Monitoring flow
FastAPI Backend
      |
      v
 /metrics
      |
      v
Prometheus
      |
      v
Grafana

Implemented activities:

FastAPI metrics instrumentation
Prometheus configuration
Metrics collection
Grafana configuration
Dashboard creation
Backend CPU and memory monitoring

Prometheus is used for metrics collection and Grafana is used for visualization.

🔐 9. Security Scanning — Trivy

Trivy was integrated into the Jenkins pipeline for container image vulnerability scanning.

Pipeline flow:

Docker Build
     |
     v
Container Image
     |
     v
Trivy Scan
     |
     v
Vulnerability Report

The pipeline scans container images for:

HIGH vulnerabilities
CRITICAL vulnerabilities

The scan is currently configured as a non-blocking security check so that vulnerability findings are reported as part of the CI/CD workflow.

The presence of a security scan does not mean that all vulnerabilities are automatically fixed. Scan results should be reviewed and remediated as part of an ongoing security process.

🧪 10. Testing

The backend contains an automated test suite using pytest.

cd backend
pytest

The current test suite contains:

26 tests

Tests run against an isolated in-memory SQLite database configured for the test environment, so the test suite does not require an external PostgreSQL instance.

Test coverage areas
User registration
Duplicate email rejection
Login success/failure
Authentication requirements
Health endpoint
Database health endpoint
Task creation
Task retrieval
Task listing
Invalid task input
Task status updates
Invalid status rejection
Task deletion
Incident creation
Incident retrieval
Incident listing
Incident severity validation
Incident resolution
resolved_at timestamp behavior
Comments
Invalid comment entity handling
Dashboard statistics
Authentication requirements for protected dashboard routes

The test suite is also executed as part of the Jenkins CI workflow.

🛠️ Application Development & Local Setup
Prerequisites

For local development without Docker:

Python
Node.js / npm
PostgreSQL

For containerized execution:

Docker
Docker Compose
▶️ Start the application — Local Development
Backend
cd backend

python -m venv .venv

Activate the virtual environment.

Linux/macOS
source .venv/bin/activate
Windows PowerShell
.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Start the backend:

uvicorn app.main:app --reload --port 8000
Frontend

Open a separate terminal:

cd frontend
npm install
npm run dev

The frontend uses the configured VITE_API_URL to communicate with the backend.

🐳 Start the application with Docker Compose

Create the environment file:

cp .env.example .env

Then start the application:

docker compose up --build

Check running containers:

docker compose ps

Stop the application:

docker compose down
🔧 Environment Variables

The application uses environment variables for runtime configuration.

Important variables include:

Variable	Component	Description
LOG_LEVEL	Backend	Python logging level
CORS_ORIGINS	Backend	Allowed frontend origins
VITE_API_URL	Frontend	Backend API base URL
POSTGRES_USER	PostgreSQL	Database user
POSTGRES_PASSWORD	PostgreSQL	Database password
POSTGRES_DB	PostgreSQL	Database name
POSTGRES_PORT	PostgreSQL	PostgreSQL port
DATABASE_URL	Backend	Database connection string
JWT_SECRET	Backend	JWT signing secret
APP_ENV	Backend	Application environment

Use .env.example as the configuration reference.

Never commit real secrets or production credentials to the repository.

🧪 Test Command

Run the backend test suite:

cd backend
pytest

Current test suite:

26 tests

The tests use an isolated in-memory SQLite database and do not require an external PostgreSQL instance.

📚 API Documentation

Once the backend is running, interactive API documentation is available at:

Swagger UI
http://localhost:8000/api/docs
ReDoc
http://localhost:8000/api/redoc
OpenAPI Schema
http://localhost:8000/api/openapi.json
🔌 API Overview
Authentication
POST   /api/auth/register
POST   /api/auth/login
GET    /api/auth/me
Users
GET    /api/users
GET    /api/users/{id}
Tasks
GET    /api/tasks
POST   /api/tasks
GET    /api/tasks/{id}
PATCH  /api/tasks/{id}
DELETE /api/tasks/{id}

Tasks can be filtered by:

status
priority
assigned user
Incidents
GET    /api/incidents
POST   /api/incidents
GET    /api/incidents/{id}
PATCH  /api/incidents/{id}
DELETE /api/incidents/{id}

Incidents can be filtered by:

status
severity
assigned user
Comments
GET    /api/comments
POST   /api/comments
DELETE /api/comments/{id}
Dashboard
GET    /api/dashboard/stats

Most application routes require:

Authorization: Bearer <token>

Public routes include:

/
 /health
 /health/db
 /api/auth/register
 /api/auth/login
❤️ Health Endpoints

Health endpoints are specifically implemented to support deployment and DevOps workflows such as container health checks and Kubernetes probes.

Liveness
GET /health

Checks whether the application process is running and serving requests.

Returns:

200

when the application is running.

Database Readiness
GET /health/db

Checks whether the backend can reach PostgreSQL.

Successful response:

200

with database connectivity information.

If the database cannot be reached:

503

This endpoint is useful for readiness checks during containerized and Kubernetes deployments.

📝 Logging

The backend writes structured single-line log entries to standard output.

Logged events include:

HTTP requests
HTTP method
Request path
Status code
Request duration
Client information
Application startup/shutdown
User registration
Login success/failure
Task creation/update/deletion
Incident creation/update/deletion
Comment creation
Unhandled exceptions with traceback

Logs currently go to stdout.

No centralized log shipping or log aggregation system such as ELK, Loki, or CloudWatch is implemented.

Prometheus and Grafana are used separately for application metrics and monitoring.

🔍 Build Commands
Backend Docker image
docker build -t opstrack-backend ./backend
Frontend Docker image

The frontend API URL is provided during the image build:

docker build \
  --build-arg VITE_API_URL=https://your-api.example.com \
  -t opstrack-frontend \
  ./frontend
▶️ Runtime Example
Backend container
docker run -p 8000:8000 \
  -e DATABASE_URL=... \
  -e JWT_SECRET=... \
  -e APP_ENV=production \
  opstrack-backend

The exact runtime environment should be configured using the appropriate environment variables for the target environment.

🔐 Authentication

OpsTrack uses JWT bearer authentication.

Authenticated API requests use:

Authorization: Bearer <token>

The application uses stateless JWT-based authentication rather than server-side sessions.

📈 Scalability Considerations

The backend is designed without server-side session state, which allows multiple backend replicas to run behind a load balancer.

The frontend is a static SPA build served by Nginx.

The frontend's VITE_API_URL is baked into the frontend build, so a new frontend image build is required if the backend's public URL changes.

CORS is controlled through the CORS_ORIGINS environment variable and should be updated according to the environment in which the frontend is hosted.

⚠️ Known Limitations

The project intentionally keeps the application and infrastructure relatively simple so that the DevOps workflow can remain the primary focus.

Current application limitations include:

No database migration tool; schema changes currently require database reset or manual migration work.
No rate limiting.
No CSRF protection beyond JWT bearer authentication.
No refresh-token mechanism.
No file/image attachments for tasks or incidents.
No role-based access control; authenticated users can view and edit tasks/incidents according to the application's current authorization model.
No pagination on list endpoints.
No centralized log shipping or aggregation.
No distributed tracing.
No alerting system such as Alertmanager is implemented.
Prometheus and Grafana are used for application metrics and visualization.
The Kubernetes environment is based on Minikube for hands-on deployment and validation rather than a production Kubernetes cluster.
🧭 DevOps Workflow Summary

The complete hands-on workflow implemented in this project is:

Developer
    |
    v
GitHub
    |
    v
Jenkins
    |
    +--> Run 26 Backend Tests
    |
    +--> Build Docker Images
    |
    +--> Trivy Vulnerability Scan
    |
    +--> Ansible Deployment
    |
    +--> Deployment Verification
    |
    +----------------------+
                           |
              +------------+------------+
              |                         |
              v                         v
          AWS EC2                 Kubernetes
              |                     + Helm
              v                         |
            Nginx                      v
              |                   Application
        +-----+-----+
        |           |
        v           v
    Frontend     Backend
                    |
                    v
                PostgreSQL

Backend
   |
   v
Prometheus
   |
   v
Grafana
🧰 Technology Stack
Category	Technologies
Frontend	React, Vite
Backend	FastAPI, Python
Database	PostgreSQL
Testing	Pytest
Source Control	Git, GitHub
CI/CD	Jenkins
Containers	Docker, Docker Compose
Web Server	Nginx
Cloud	AWS EC2
Infrastructure as Code	Terraform
Configuration Automation	Ansible
Orchestration	Kubernetes, Minikube
Kubernetes Packaging	Helm
Security Scanning	Trivy
Monitoring	Prometheus, Grafana
Configuration	YAML, JSON, Environment Variables
🎓 Project Learning Outcomes

Through OpsTrack, the following DevOps practices were implemented and validated hands-on:

Git-based development workflow
Jenkins Pipeline as Code
Automated testing
Docker image creation
Docker Compose orchestration
CI/CD deployment automation
AWS EC2 deployment
Nginx routing
Terraform infrastructure import and validation
Ansible configuration automation
Kubernetes deployments and services
Kubernetes health probes
Kubernetes scaling
Helm deployments and rollback
Container vulnerability scanning with Trivy
Prometheus metrics collection
Grafana monitoring dashboards
Deployment verification
Failure troubleshooting and rollback
🚀 Future Improvements

Potential future improvements include:

Database migrations using Alembic
Centralized logging using Loki/ELK/CloudWatch
Alerting using Alertmanager
Distributed tracing
Role-based access control
API rate limiting
Pagination
Persistent Kubernetes database storage
Production-grade Kubernetes infrastructure
Automated vulnerability remediation workflow
Advanced CI/CD quality gates
Infrastructure provisioning from scratch using Terraform
📌 Project Status

OpsTrack currently serves as a hands-on DevOps and Cloud deployment project covering:

Git
  ↓
GitHub
  ↓
Jenkins
  ↓
Testing
  ↓
Docker
  ↓
Trivy
  ↓
AWS EC2
  ↓
Nginx
  ↓
Ansible
  ↓
Kubernetes
  ↓
Helm
  ↓
Prometheus
  ↓
Grafana

The project is intentionally documented with its current capabilities and limitations rather than presenting the environment as a production platform.

👨‍💻 Author

Abhishek Singh Chauhan

DevOps & Cloud

GitHub:
https://github.com/abhisheksinghc871-rgb

Project Repository:
https://github.com/abhisheksinghc871-rgb/opstrack
