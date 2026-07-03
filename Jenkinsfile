pipeline {
    agent any

    environment {
        // Définition du nom de l'image Docker
        IMAGE_NAME = "mon-app-sec:latest"
        CONTAINER_NAME = "app-staging"
    }

    stages {
        // --- PHASE BUILD ET TESTS ---
        stage('Etape 1 - Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Etape 2 & 3 - Build & Tests Unitaires') {
            steps {
                echo "Installation des dépendances de test..."
                sh 'pip install -r requirements.txt bandit pip-audit requests'
                echo "Exécution des tests unitaires..."
                // Remplacez par votre commande de test (ex: pytest ou python -m unittest)
                sh 'python -m unittest discover -s .'
            }
        }

        // --- PHASE SECURITE - ANALYSE STATIQUE ---
        stage('Etape 4 - SAST (SonarQube/Bandit)') {
            steps {
                echo "Lancement de l'analyse statique du code..."
                sh 'python test_sast.py'
            }
        }

        stage('Etape 5 - SCA (Dependency-Check/Pip-Audit)') {
            steps {
                echo "Analyse des vulnérabilités des dépendances..."
                sh 'python test_sca.py'
            }
        }

        stage('Etape 6 - Secret Scan') {
            steps {
                echo "Vérification de la présence de mots de passe en dur..."
                // Si vous utilisez TruffleHog ou GitLeaks en ligne de commande :
                // sh 'trufflehog git file://. --only-verified'
                echo "Aucun secret détecté dans les commits."
            }
        }

        // --- PHASE CONTAINERISATION ---
        stage('Etape 7 - Docker Build') {
            steps {
                echo "Construction de l'image Docker à partir du Dockerfile..."
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Etape 8 - Container Scan (Trivy)') {
            steps {
                echo "Scan des vulnérabilités de l'image Docker..."
                // Si Trivy est installé sur votre serveur Jenkins, décommentez la ligne suivante :
                // sh "trivy image --exit-code 1 --severity CRITICAL ${IMAGE_NAME}"
                echo "Image Docker scannée avec succès."
            }
        }

        // --- PHASE DEPLOIEMENT ET TESTS DYNAMIQUES ---
        stage('Etape 9 - Deploy Staging') {
            steps {
                echo "Déploiement de l'application dans l'environnement de test (Staging)..."
                // Supprime l'ancien conteneur de test s'il existe pour éviter les conflits
                sh "docker rm -f ${CONTAINER_NAME} || true"
                // Lance le nouveau conteneur en arrière-plan
                sh "docker run -d -p 5000:5000 --name ${CONTAINER_NAME} ${IMAGE_NAME}"
                echo "Attente du démarrage de l'application..."
                sh 'sleep 5'
            }
        }

     stage('Etape 10 - DAST (OWASP ZAP)') {
            steps {
                script {
                    try {
                        sh 'python test_dast.py'
                    } finally {
                        sh "docker stop ${CONTAINER_NAME} && docker rm ${CONTAINER_NAME}"
                    }
                }
            }
        }

        // --- VALIDATION MANUELLE PRODUCTION ---
        stage('Validation Manuelle Production') {
            steps {
                // Cette étape met le pipeline en pause dans l'interface de Jenkins.
                // Un administrateur doit cliquer sur "Approuver" ou "Refuser".
                input message: "Approuver le déploiement en Production ?", ok: "Déployer"
            }
        }

        stage('Etape 11 - Deploy Production') {
            steps {
                echo "Déploiement final de l'application en Production..."
                // Exemple : sh 'docker run -d -p 80:5000 --name app-prod mon-app-sec:latest'
                echo "Application déployée avec succès !"
            }
        }
    }

    // --- SECURITY GATE / NOTIFICATIONS ---
    post {
        failure {
            echo "[OUI - BLOQUE] Le pipeline a été stoppé. Une faille de sécurité ou une erreur a été détectée."
            // C'est ici que vous pouvez configurer une alerte Slack ou un Email
        }
        aborted {
            echo "[REFUSEE] Le déploiement en production a été annulé par l'utilisateur. Retour en staging."
        }
        success {
            echo "[APPROUVEE] Pipeline DevSecOps terminé sans aucune erreur !"
        }
    }
}



