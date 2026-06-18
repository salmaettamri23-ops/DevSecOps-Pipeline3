pipeline {
    agent any

    stages {
        stage('1. Récupération du Code') {
            steps {
                checkout scm
            }
        }

        stage('2. Scan de Sécurité du Code (SAST)') {
            agent {
                // Jenkins va télécharger temporairement l'image officielle de sécurité Python
                docker { image 'pipelinecomponents/bandit:latest' }
            }
            steps {
                echo 'Lancement du scan de sécurité avec Bandit...'
                // Exécute le scan directement dans l'environnement sécurisé
                sh 'bandit -r app.py'
            }
        }

        stage('3. Analyse des Dépendances (SCA)') {
            agent {
                // Jenkins télécharge l'image officielle de l'outil Trivy
                docker { image 'aquasec/trivy:latest' }
            }
            steps {
                echo 'Analyse du fichier requirements.txt...'
                sh 'trivy fs --exit-code 0 requirements.txt'
            }
        }

        stage('4. Construction de l\'image Docker') {
            steps {
                echo 'Construction de l\'image de l\'application...'
                sh 'docker build -t mon-app-sec:latest .'
            }
        }

        stage('5. Scan de l\'image Docker') {
            agent {
                docker { image 'aquasec/trivy:latest' }
            }
            steps {
                echo 'Analyse des vulnérabilités de l\'image finale...'
                sh 'trivy image --exit-code 0 mon-app-sec:latest'
            }
        }

        stage('6. Déploiement Sécurisé') {
            steps {
                echo 'Déploiement de l\'application...'
                sh 'docker rm -f app-securisee || true'
                sh 'docker run -d --name app-securisee -p 5000:5000 mon-app-sec:latest'
            }
        }
    }
}
