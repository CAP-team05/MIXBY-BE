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
                sh 'make clean'
                sh 'make build'
                sh 'make run'
            }
        }
    }
}