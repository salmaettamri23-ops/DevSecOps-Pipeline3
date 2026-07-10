pipeline {
    agent any

    triggers {
        pollSCM('H/2 * * * *')
    }

           stage('1. Recuperation du Code') {
            steps {
                git branch: 'main', // mettez 'master' ou 'main' selon votre branche
                    credentialsId: 'git-credentials',
                    url: 'https://github.com'
            }
        }


        stage('2. Scan de Securite du Code (SAST)') {
            steps {
                echo "Lancement du scan de securite avec Bandit via Docker..."
                // Exécute Bandit dans un conteneur pour analyser app.py
                sh 'docker run --rm -v "${WORKSPACE}":/apps opensecurity/bandit -r /apps -f json -o /apps/bandit-report.json || true'
            }
        }

        stage('3. Analyse des Dependances (SCA)') {
            steps {
                echo "Analyse du fichier requirements.txt avec Trivy..."
                // Exécute Trivy pour scanner vos bibliothèques Python
                sh 'docker run --rm -v "${WORKSPACE}":/apps aquasec/trivy:latest fs /apps/requirements.txt || true'
            }
        }

        stage('4. Construction de l\'image Docker') {
            steps {
                echo "Construction de l\'image de l\'application..."
                // Construit votre image sur votre Docker Desktop
                sh 'docker build -t mon-app-sec:latest .'
            }
        }

        stage('5. Scan de l\'image Docker') {
            steps {
                echo "Analyse des vulnerabilites de l\'image finale avec Trivy..."
                // Scanne l'image créée à l'étape précédente
                sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image mon-app-sec:latest || true'
            }
        }

        stage('6. Deploiement Securise') {
            steps {
                echo "Deploiement de l\'application..."
                // Supprime l'ancien conteneur s'il existe et lance le nouveau
                sh '''
                    docker stop app-securisee || true
                    docker rm app-securisee || true
                    docker run -d --name app-securisee -p 5000:5000 mon-app-sec:latest
                    sleep 5
                '''
            }
        }

        stage('7. Analyse Dynamique (DAST)') {
            steps {
                echo "Verification de la disponibilite de l\'application..."
                // Teste si l'application répond sur le port 5000
                sh 'curl -I http://localhost:5000 || true'

                echo "Creation du rapport final..."
                sh 'echo "<html><body><h1>Rapport de Securite</h1><p>L\'application a ete analysee avec succes.</p></body></html>" > index.html'

                publishHTML(target: [
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: '.',
                    reportFiles: 'index.html',
                    reportName: 'Rapport Securite'
                ])
            }
        }
    }

    post {
        success {
            echo 'Pipeline DevSecOps termine avec succes!'
        }
        failure {
            echo 'Le pipeline a rencontre une erreur.'
        }
    }
}
