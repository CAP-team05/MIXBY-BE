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
                    branches: [[name: '*/main']],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [[$class: 'LocalBranch', localBranch: 'main']],
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
                  -p ${SERVER_PORT:-5050}:${SERVER_PORT:-5050} \
                  -e SERVER_PORT=${SERVER_PORT:-5050} \
                  -e API_PORT=${SERVER_PORT:-5050} \
                  mixby-api:latest
                '''
            }
        }
    }
}