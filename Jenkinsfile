pipeline {
    agent any
    stages {
        stage('Cleanup') {
            steps {
                deleteDir()
            }
        }
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM',
                    branches: [[name: '*/ahn']],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [[$class: 'LocalBranch', localBranch: 'ahn']],
                    userRemoteConfigs: [[url: 'git@github.com:CAP-team05/MIXBY-BE.git']]
                ])
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