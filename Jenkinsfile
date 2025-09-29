pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'git@github.com:ORG/REPO.git'
            }
        }
        stage('Build & Deploy') {
            steps {
                sh '''
                echo "🛑 Stopping old container..."
                docker stop mixby-container || true
                docker rm mixby-container || true

                echo "📦 Building new image (latest)..."
                docker build -t mixby-api:latest .

                echo "🚀 Starting new container..."
                docker run -d --name mixby-container \
                  -p ${SERVER_PORT:-8080}:${SERVER_PORT:-8080} \
                  -e SERVER_PORT=${SERVER_PORT:-8080} \
                  -e API_PORT=${SERVER_PORT:-8080} \
                  mixby-api:latest
                '''
            }
        }
    }
}