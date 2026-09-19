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
    }

    post {
        success {
            echo 'OpsTrack CI Pipeline: SUCCESS'
        }
        failure {
            echo 'OpsTrack CI Pipeline: FAILED'
        }
    }
}
