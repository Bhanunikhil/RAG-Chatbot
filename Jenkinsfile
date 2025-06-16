// Jenkinsfile

pipeline {
    agent any // This pipeline can run on any available Jenkins agent

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
                // Run the pytest suite. (This will run the test we defined earlier)
                sh 'pytest'
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