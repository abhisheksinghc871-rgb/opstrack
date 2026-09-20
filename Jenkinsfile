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
	stage('Security Scan - Trivy') {
	    steps {
	        sh '''
	            trivy image \
	              --severity HIGH,CRITICAL \
	              --exit-code 0 \
	              opstrack-backend:ci

	            trivy image \
	              --severity HIGH,CRITICAL \
	              --exit-code 0 \
	              opstrack-frontend:ci
	        '''
	    }
	}

        stage('Terraform Validate') {
    	    steps {
        	sh '''
            	    cd terraform
                    terraform init -backend=false -input=false
                    terraform fmt -check
                    terraform validate
                '''
             }
         }

        stage('Deploy') {
	     steps {
                 sh '''
		     ansible-playbook \
                     -i /home/ubuntu/opstrack/ansible/inventory \
                     /home/ubuntu/opstrack/ansible/deploy.yml
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
