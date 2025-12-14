pipeline {
    agent any

    environment {
        // Define environment variables if needed
        IMAGE_NAME = "canc-app"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Try to build the image. caching might be effective if set up, 
                    // but for simplicity we verify the build here.
                    sh "docker build -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Run pytest inside the container
                    // We mount the current directory to run tests that might have changed
                    sh """
                    docker run --rm -e PYTHONPATH=. ${IMAGE_NAME}:latest pytest tests/
                    """
                }
            }
        }
    }

    post {
        always {
            // Clean up could happen here if needed, e.g. docker rmi
            echo 'Pipeline finished'
        }
        success {
            echo 'Build and Test succeeded!'
        }
        failure {
            echo 'Pipeline failed'
        }
    }
}
