pipeline {
    agent any
    stages {
        stage('1. Recuperation du Code') {
            steps {
                echo 'Etape Git sautee : Lecture du code locale'
            }
        }

        stage('2. Scan de Securite du Code (SAST)') {
            steps {
                echo 'Lancement du scan avec Bandit (via Docker)...'
                sh 'docker run --rm -v "$(pwd)":/apps pysec/bandit -r /apps/app.py || true'
            }
        }

        stage('3. Analyse des Dependances (SCA)') {
            steps {
                echo 'Analyse du fichier requirements.txt avec Trivy...'
                sh 'docker run --rm -v "$(pwd)":/apps aquasec/trivy fs /apps/requirements.txt || true'
            }
        }

        stage('4. Construction de l\'image Docker') {
            steps {
                echo 'Construction de l\'image de l\'application...'
                sh 'docker build -t mon-app-sec:latest . || true'
            }
        }

        stage('5. Scan de l\'image Docker') {
            steps {
                echo 'Analyse des vulnerabilites de l\'image finale...'
                sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image mon-app-sec:latest || true'
            }
        }

        stage('6. Deploiement Securise') {
            steps {
                echo 'Deploiement de l\'application...'
                sh 'docker rm -f app-securisee || true'
                sh 'docker run -d --name app-securisee -p 5000:5000 mon-app-sec:latest || true'
            }
        }

         stage('7. Analyse Dynamique (DAST)') {
            steps {
                echo 'Verification de la disponibilite de l\'application...'
                sh 'curl -I http://localhost:5000 || true'

                echo 'Lancement du VRAI scan de securite OWASP ZAP dans Docker...'
                // Remplacement de la simulation par la vraie commande ZAP
                sh 'docker run --rm -v "$(pwd)":/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t http://localhost:5000 -r rapport_zap.html || true'

                publishHTML([
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: '.',
                    reportFiles: 'rapport_zap.html',
                    reportName: 'Rapport Securite OWASP ZAP',
                    reportTitles: 'Rapport ZAP'
                ])
            }
        }
    }
}
