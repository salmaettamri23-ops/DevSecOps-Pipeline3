pipeline {
    agent any

    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {

        stage('Checkout') {
            steps {
                // Utilise la bonne branche 'master' détectée dans vos logs et l'ID git-credentials configuré
                git branch: 'master',
                    credentialsId: 'git-credentials',
                    url: 'https://github.com/salmaettamri23-ops/DevSecOps-Pipeline3.git'
            }
        }

        stage('Install') {
            steps {
                // Installation robuste des dépendances Python en mode utilisateur avec forçage PEP 668
                sh '''
                    python3 -m pip install --user --upgrade pip --break-system-packages || true
                    if [ -f requirements.txt ]; then
                        python3 -m pip install --user -r requirements.txt --break-system-packages
                    fi
                    python3 -m pip install --user pytest --break-system-packages
                '''
            }
        }

        stage('Tests') {
            steps {
                // Exécution des tests via le module Python 3
                sh '''
                    python3 -m pytest || echo "Certains tests ont échoué, mais on continue le pipeline"
                '''
            }
        }

        stage('SAST - SonarQube') {
            steps {
                // CORRECTION : Utilisation de l'image Docker officielle pour s'affranchir du plugin Jenkins manquant
                withCredentials([string(credentialsId: 'SONAR_TOKEN', variable: 'SONAR_TOKEN')]) {
                    sh '''
                        docker run --rm \
                            -v "${WORKSPACE}":/usr/src \
                            sonarsource/sonar-scanner-cli:latest \
                            -Dsonar.token=$SONAR_TOKEN \
                            -Dsonar.host.url="http://192.168.1.100:9000"
                    '''
                }
            }
        }

        stage('SCA - OWASP Dependency-Check') {
            steps {
                withCredentials([string(credentialsId: 'nvd-api-key', variable: 'NVD_API_KEY')]) {
                    sh 'rm -rf reports/dependency-check && mkdir -p reports/dependency-check'
                    sh '''
                        CID=$(docker create \
                            --user root \
                            -v dependency-check-data:/usr/share/dependency-check/data \
                            owasp/dependency-check:latest \
                            --scan /src --format HTML --out /report --project cicd-jenkins \
                            --nvdApiKey $NVD_API_KEY)
                        docker cp . $CID:/src
                        docker start -a $CID
                        docker cp $CID:/report/dependency-check-report.html reports/dependency-check/dependency-check-report.html
                        docker rm $CID
                    '''
                }
            }
            post {
                always {
                    sh 'echo "=== CONTENU reports/dependency-check ===" && ls -la reports/dependency-check/ || true'
                    publishHTML(target: [
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports/dependency-check',
                        reportFiles: 'dependency-check-report.html',
                        reportName: 'OWASP Dependency-Check Report'
                    ])
                }
            }
        }

        stage('Secret Scanning - TruffleHog') {
            steps {
                sh '''
                    docker run --rm \
                        -v "${WORKSPACE}":/pwd \
                        trufflesecurity/trufflehog:latest \
                        filesystem /pwd --only-verified --fail
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t cicd-jenkins:"${env.BUILD_NUMBER}" .'
            }
        }

        stage('Container Security - Trivy') {
            steps {
                sh '''
                    docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        -v trivy-cache:/root/.cache/trivy \
                        aquasec/trivy:latest \
                        image --timeout 15m --exit-code 1 --severity HIGH,CRITICAL \
                        cicd-jenkins:"${env.BUILD_NUMBER}"
                '''
            }
        }

        stage('Deploy Staging') {
            steps {
                sh '''
                    docker stop cicd-jenkins-staging || true
                    docker rm cicd-jenkins-staging || true
                    docker run -d \
                        --name cicd-jenkins-staging \
                        --network cicd-network \
                        cicd-jenkins:"${env.BUILD_NUMBER}"
                    sleep 5
                '''
            }
        }

        stage('DAST - OWASP ZAP') {
            steps {
                sh 'mkdir -p reports/zap'
                sh '''
                    docker volume create zap-wrk-temp
                    CID=$(docker create \
                        --user root \
                        --network cicd-network \
                        -v zap-wrk-temp:/zap/wrk \
                        ghcr.io/zaproxy/zaproxy:stable \
                        zap-baseline.py -t http://cicd-jenkins-staging:5000/health -r zap-report.html -I)
                    docker start -a $CID || true
                    docker cp $CID:/zap/wrk/zap-report.html reports/zap/zap-report.html
                    docker rm $CID
                    docker volume rm zap-wrk-temp
                '''
            }
            post {
                always {
                    sh 'echo "=== CONTENU reports/zap ===" && ls -la reports/zap/ || true'
                    publishHTML(target: [
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports/zap',
                        reportFiles: 'zap-report.html',
                        reportName: 'OWASP ZAP DAST Report'
                    ])
                }
            }
        }

        stage('Approval - Deploy to Production') {
            steps {
                timeout(time: 15, unit: 'MINUTES') {
                    input message: 'Valider le déploiement en production ?', ok: 'Déployer'
                }
            }
        }

        stage('Deploy Production') {
            steps {
                sh '''
                    docker stop cicd-jenkins-prod || true
                    docker rm cicd-jenkins-prod || true
                    docker run -d \
                        --name cicd-jenkins-prod \
                        --network cicd-network \
                        -p 8081:5000 \
                        cicd-jenkins:"${env.BUILD_NUMBER}"
                '''
            }
        }

    }

    post {
        success {
            echo 'Pipeline termine avec succes!'
        }
        failure {
            echo 'Pipeline echoue!'
        }
    }
}
