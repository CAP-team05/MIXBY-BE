pipeline {
    agent any
    parameters {
        string(name: 'API_PORT', defaultValue: '', description: 'Optional override when .env is not present')
        string(name: 'DOTENV_CREDENTIALS_ID', defaultValue: 'mixby-dotenv', description: 'Secret file credential ID that contains .env')
        booleanParam(name: 'ENABLE_ROLLBACK', defaultValue: true, description: 'Enable rollback to last successful build on failure')
    }
    environment {
        LAST_SUCCESSFUL_COMMIT = ''
        CURRENT_COMMIT = ''
    }
    stages {
        stage('Prepare') {
            steps {
                script {
                    // 현재 커밋 저장
                    env.CURRENT_COMMIT = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                    echo "Current commit: ${env.CURRENT_COMMIT}"

                    // 마지막 성공한 빌드의 커밋 찾기
                    def lastSuccessfulBuild = currentBuild.getPreviousSuccessfulBuild()
                    if (lastSuccessfulBuild != null) {
                        env.LAST_SUCCESSFUL_COMMIT = lastSuccessfulBuild.description?.tokenize('|')?.find { it.startsWith('commit:') }?.split(':')?.last()?.trim()
                        if (!env.LAST_SUCCESSFUL_COMMIT) {
                            // description에서 찾지 못했다면 빌드 환경변수에서 찾기
                            def lastBuildEnvVars = lastSuccessfulBuild.getEnvironment()
                            env.LAST_SUCCESSFUL_COMMIT = lastBuildEnvVars.get('GIT_COMMIT')
                        }
                        if (env.LAST_SUCCESSFUL_COMMIT) {
                            echo "Last successful commit: ${env.LAST_SUCCESSFUL_COMMIT}"
                        } else {
                            echo "Could not determine last successful commit"
                        }
                    } else {
                        echo "No previous successful build found"
                    }
                }
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
                script {
                    // 체크아웃 후 현재 커밋 다시 확인
                    env.CURRENT_COMMIT = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                    // 빌드 description에 커밋 정보 저장
                    currentBuild.description = "commit:${env.CURRENT_COMMIT}"
                    echo "Updated current commit: ${env.CURRENT_COMMIT}"
                }
            }
        }
        stage('Load Env') {
            steps {
                script {
                    def credentialId = (params.DOTENV_CREDENTIALS_ID ?: env.DOTENV_CREDENTIALS_ID)?.trim()
                    if (credentialId) {
                        withCredentials([file(credentialsId: credentialId, variable: 'DOTENV_FILE')]) {
                            def dotenvContent = readFile(env.DOTENV_FILE)

                            // .env 파일을 작업 디렉토리에 복사
                            writeFile file: '.env', text: dotenvContent
                            echo '.env file created from credentials'

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
        always {
            // 보안을 위해 .env 파일 정리
            sh 'rm -f .env'
            echo '.env file cleaned up'
        }
        success {
            emailext(
                subject: "✅ SUCCESS: MIXBY-BE Build #${BUILD_NUMBER}",
                body: "빌드 성공!\n커밋: ${env.CURRENT_COMMIT}\n자세히 보기: ${BUILD_URL}",
                to: "cau.snsn@gmail.com, ahnjh05141@naver.com, handlecu@gmail.com"
            )
        }
        failure {
            script {
                def rollbackPerformed = false

                // Rollback 기능이 활성화되고 마지막 성공 커밋이 있는 경우에만 실행
                if (params.ENABLE_ROLLBACK && env.LAST_SUCCESSFUL_COMMIT && env.LAST_SUCCESSFUL_COMMIT != env.CURRENT_COMMIT) {
                    try {
                        echo "🔄 빌드 실패! 마지막 성공 버전으로 롤백 시도 중..."
                        echo "롤백 대상: ${env.LAST_SUCCESSFUL_COMMIT}"

                        // 마지막 성공한 커밋으로 체크아웃
                        sh "git checkout ${env.LAST_SUCCESSFUL_COMMIT}"

                        // .env 파일 재생성 (credentials 재로드)
                        def credentialId = (params.DOTENV_CREDENTIALS_ID ?: env.DOTENV_CREDENTIALS_ID)?.trim()
                        if (credentialId) {
                            withCredentials([file(credentialsId: credentialId, variable: 'DOTENV_FILE')]) {
                                def dotenvContent = readFile(env.DOTENV_FILE)
                                writeFile file: '.env', text: dotenvContent
                                echo '.env file recreated for rollback'
                            }
                        }

                        // 롤백 빌드 및 배포
                        sh 'make stop'
                        sh 'make clean'
                        sh 'make build'
                        sh 'make run'

                        rollbackPerformed = true
                        echo "✅ 롤백 성공: ${env.LAST_SUCCESSFUL_COMMIT}"

                    } catch (Exception e) {
                        echo "❌ 롤백 실패: ${e.getMessage()}"
                        echo "수동 복구가 필요합니다"
                    } finally {
                        // 롤백 시도 후에도 .env 파일 정리
                        sh 'rm -f .env'
                    }
                }

                // 실패 알림 이메일
                def emailBody = "빌드 실패...\n커밋: ${env.CURRENT_COMMIT}\n로그 확인: ${BUILD_URL}\n"
                if (rollbackPerformed) {
                    emailBody += "\n🔄 자동 롤백 완료: ${env.LAST_SUCCESSFUL_COMMIT}"
                } else if (params.ENABLE_ROLLBACK && env.LAST_SUCCESSFUL_COMMIT) {
                    emailBody += "\n❌ 롤백 실패 또는 불가능"
                } else {
                    emailBody += "\n⚠️ 롤백 비활성화 또는 이전 성공 빌드 없음"
                }

                emailext(
                    subject: "❌ FAILURE: MIXBY-BE Build #${BUILD_NUMBER}${rollbackPerformed ? ' (Rollback Applied)' : ''}",
                    body: emailBody,
                    to: "cau.snsn@gmail.com, ahnjh05141@naver.com, handlecu@gmail.com"
                )
            }
        }
    }
}
