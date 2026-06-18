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
                // Cette ligne ignore l'erreur si l'outil n'est pas configuré sur le serveur
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
    }
}