pipeline {
    agent any
    stages {
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
        stage('Load Env') {
            steps {
                sh 'export $(grep -v "^#" .env | xargs)'
            }
        }
        stage('Build & Deploy') {
            steps {
                sh 'make stop'
                sh 'make clean'
                sh 'make build'
                sh 'make run'
            }
        }
    }
    post {
        success {
            emailext(
                subject: "✅ SUCCESS: MIXBY-BE Build #${BUILD_NUMBER}",
                body: "빌드 성공!\n자세히 보기: ${BUILD_URL}",
                to: "ahnjh05141@naver.com, handlecu@gmail.com"
            )
        }
        failure {
            emailext(
                subject: "❌ FAILURE: MIXBY-BE Build #${BUILD_NUMBER}",
                body: "빌드 실패...\n로그 확인: ${BUILD_URL}",
                to: "ahnjh05141@naver.com, handlecu@gmail.com"
            )
        }
    }
}