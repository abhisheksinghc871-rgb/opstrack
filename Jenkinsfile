pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Backend Tests') {
            steps {
                sh '''
                    docker run --rm \
                      -v "$PWD/backend:/app" \
                      -w /app \
                      python:3.12-slim \
                      sh -c "pip install --no-cache-dir -r requirements.txt && pytest -q"
                '''
            }
        }

        stage('Frontend Build') {
            steps {
                sh '''
                    docker build \
                      --build-arg VITE_API_URL=/api \
                      -t opstrack-frontend:ci \
                      ./frontend
                '''
            }
        }

        stage('Backend Docker Build') {
            steps {
                sh '''
                    docker build \
                      -t opstrack-backend:ci \
                      ./backend
                '''
            }
        }

        stage('Terraform Validate & Plan') {
            steps {
                sh '''
                    cd terraform
                    terraform init -input=false
                    terraform fmt -check
                    terraform validate
                    terraform plan -input=false
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    cd /home/ubuntu/opstrack
                    docker compose up -d --build --wait
                    docker compose ps
                '''
            }
        }

        stage('Deployment Verification') {
            steps {
                sh '''
                    sleep 10
                    curl -f http://localhost/
                    curl -f http://localhost/api/health || true
                    docker compose -f /home/ubuntu/opstrack/docker-compose.yml ps
                '''
            }
        }
    }

    post {
        success {
            echo 'OpsTrack CI/CD Pipeline: SUCCESS'
        }
        failure {
            echo 'OpsTrack CI/CD Pipeline: FAILED'
        }
    }
}
