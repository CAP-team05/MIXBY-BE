pipeline {
    agent any
    parameters {
        string(name: 'API_PORT', defaultValue: '', description: 'Optional override when .env is not present')
        string(name: 'DOTENV_CREDENTIALS_ID', defaultValue: 'mixby-dotenv', description: 'Secret file credential ID that contains .env')
    }
    stages {
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
        stage('Load Env') {
            steps {
                script {
                    def credentialId = (params.DOTENV_CREDENTIALS_ID ?: env.DOTENV_CREDENTIALS_ID)?.trim()
                    if (credentialId) {
                        withCredentials([file(credentialsId: credentialId, variable: 'DOTENV_FILE')]) {
                            def dotenvContent = readFile(env.DOTENV_FILE)
                            def apiPortFromSecret = null
                            dotenvContent
                                .split("\r?\n")
                                .each { line ->
                                    if (!apiPortFromSecret) {
                                        def trimmed = line.trim()
                                        if (trimmed && !trimmed.startsWith('#') && trimmed.contains('=')) {
                                            def parts = trimmed.split('=', 2)
                                            if (parts[0] == 'API_PORT') {
                                                apiPortFromSecret = parts[1]?.trim()
                                            }
                                        }
                                    }
                                }

                            if (apiPortFromSecret) {
                                echo 'API_PORT pulled from secret file.'
                                env.API_PORT = apiPortFromSecret
                            } else {
                                echo 'API_PORT not found in secret file; awaiting other sources.'
                            }
                        }
                    } else {
                        echo 'DOTENV credential ID missing; continuing with Jenkins-provided environment variables only.'
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
