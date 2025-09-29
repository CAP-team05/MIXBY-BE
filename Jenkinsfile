pipeline {
    agent any
    parameters {
        string(name: 'API_PORT', defaultValue: '', description: 'Optional override when .env is not present')
        string(name: 'DOTENV_CREDENTIALS_ID', defaultValue: '', description: 'Secret file credential ID that contains .env')
    }
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
                script {
                    if (!fileExists('.env')) {
                        def credentialId = (params.DOTENV_CREDENTIALS_ID ?: env.DOTENV_CREDENTIALS_ID)?.trim()
                        if (credentialId) {
                            withCredentials([file(credentialsId: credentialId, variable: 'DOTENV_FILE')]) {
                                sh 'cp "$DOTENV_FILE" .env'
                            }
                        } else {
                            echo '.env file not found; continuing with Jenkins-provided environment variables only.'
                        }
                    }

                    if (fileExists('.env')) {
                        readFile('.env')
                            .split("\r?\n")
                            .each { line ->
                                def trimmed = line.trim()
                                if (trimmed && !trimmed.startsWith('#') && trimmed.contains('=')) {
                                    def parts = trimmed.split('=', 2)
                                    env[parts[0]] = parts[1]
                                }
                            }
                    }

                    if (params.API_PORT?.trim()) {
                        env.API_PORT = params.API_PORT.trim()
                    }

                    if (env.API_PORT) {
                        echo "Loaded API_PORT=${env.API_PORT}"
                    } else {
                        env.API_PORT = '8080'
                        echo 'API_PORT not defined; defaulting to 8080.'
                    }
                }
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
                to: "cau.snsn@gmailcom, ahnjh05141@naver.com, handlecu@gmail.com"
            )
        }
        failure {
            emailext(
                subject: "❌ FAILURE: MIXBY-BE Build #${BUILD_NUMBER}",
                body: "빌드 실패...\n로그 확인: ${BUILD_URL}",
                to: "cau.snsn@gmail.com, ahnjh05141@naver.com, handlecu@gmail.com"
            )
        }
    }
}
