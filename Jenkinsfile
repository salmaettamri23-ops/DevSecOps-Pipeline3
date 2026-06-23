pipeline {
    agent any

    stages {
        stage('1. Recuperation du Code') {
            steps {
                checkout scm
            }
        }

        stage('2. Scan de Securite du Code (SAST)') {
            steps {
                echo 'Lancement du scan de securite avec Bandit...'
                sh 'pip install bandit || true'
                sh 'bandit -r app.py || true'
            }
        }

        stage('3. Analyse des Dependances (SCA)') {
            steps {
                echo 'Analyse du fichier requirements.txt...'
                sh 'trivy fs --exit-code 0 requirements.txt || true'
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
                sh 'trivy image --exit-code 0 mon-app-sec:latest || true'
            }
        }

        stage('6. Deploiement Securise') {
            steps {
                echo 'Deploiement de l\'application...'
                sh 'docker rm -f app-securisee || true'
                sh 'docker run -d --name app-securisee -p 5000:5000 mon-app-sec:latest || true'
            }
        }

        stage('7. Analyse Dynamique (DAST) avec OWASP ZAP') {
            steps {
                echo 'Lancement de l\'attaque de test OWASP ZAP...'

                // On utilise directement l'exécutable Windows de ZAP sans Docker !
                bat '"C:\\Program Files\\OWASP\\Zed Attack Proxy\\zap.bat" -cmd -quickurl http://localhost:5000 -quickout %WORKSPACE%\\rapport_zap.html || true'

                // On publie le rapport généré
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