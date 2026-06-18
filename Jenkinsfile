pipeline {
    agent any
    stages {
        stage('1. Récupération du Code') {
            steps {
                checkout scm
            }
        }
        stage('2. Scan de Sécurité du Code (SAST)') {
            steps {
                sh 'pip install bandit'
                sh 'bandit -r app.py'
            }
        }
        stage('3. Analyse des Dépendances (SCA)') {
            steps {
                sh 'trivy fs requirements.txt'
            }
        }
        stage('4. Construction de l\'image Docker') {
            steps {
                sh 'docker build -t mon-app-sec:latest .'
            }
        }
        stage('5. Scan de l\'image Docker') {
            steps {
                sh 'trivy image mon-app-sec:latest'
            }
        }
        stage('6. Déploiement Sécurisé') {
            steps {
                sh 'docker rm -f app-securisee || true'
                sh 'docker run -d --name app-securisee -p 5000:5000 mon-app-sec:latest'
            }
        }
    }
}
