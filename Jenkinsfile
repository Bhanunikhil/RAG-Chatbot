// Jenkinsfile

pipeline {
    agent {
        docker {
            image 'python:3.10-slim'
            args '-u root' // Run as root user inside the container to avoid permission issues
        }
    }
    stages {

        stage('Install Dependencies') {
            steps {
                // Jenkins uses 'sh' for shell commands
                sh 'pip install -r requirements.txt'
                sh 'pip install pytest pytest-mock flake8'
            }
        }

        stage('Lint Code') {
            steps {
                // Run the linter to check for code style issues
                sh 'flake8 src/ --count --exit-zero'
            }
        }

        stage('Run Unit Tests') {
            steps {
                // This flag tells pytest to exit with 0 (success) even if no tests are found.
                sh 'PYTHONPATH=. pytest --no-tests-found-exit-code=0'
            }
        }

        stage('Verify Docker Build') {
            steps {
                // As a final CI check, ensure the Dockerfile is valid and can build
                sh 'docker build -t rag-chatbot-app-test .'
            }
        }
    }
    post {
        always {
            echo 'CI pipeline finished.'
        }
    }
}