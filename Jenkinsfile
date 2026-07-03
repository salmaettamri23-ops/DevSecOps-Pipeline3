pipeline {
    // Étape générale : orchestration globale sur n'importe quel agent disponible
    agent any

    environment {
        IMAGE_NAME = "mon-app-devsecops:latest"
        CONTAINER_NAME = "app-staging-test"
        SONAR_SERVER_NAME = "SonarQube-Server" // Nom du serveur configuré dans Jenkins
    }

    stages {
        // ==========================================
        // PHASE BUILD ET TESTS (Étapes 1, 2, 3)
        // ==========================================
        stage('Phase Build et Tests') {
            steps {
                echo "Etape 1 - Checkout : Récupération du code source depuis GitHub..."
                checkout scm

                echo "Etape 2 - Build : Installation des dépendances npm et compilation..."
                sh 'npm install'

                echo "Etape 3 - Tests unitaires : Exécution des tests Jest avec couverture..."
                sh 'npm test -- --coverage'
            }
        }

        // ==========================================
        // PHASE SÉCURITÉ - ANALYSE STATIQUE (Étapes 4, 5, 6)
        // ==========================================
        stage('Phase Securite - Analyse Statique') {
            steps {
                // On regroupe les 3 analyses en parallèle ou à la suite comme sur le schéma
                echo "Etape 4 - SAST : Analyse du code source avec SonarQube..."
                withSonarQubeEnv("${SONAR_SERVER_NAME}") {
                    sh 'sonar-scanner'
                }

                echo "Etape 5 - SCA : Audit des dépendances avec OWASP Dependency-Check..."
                sh 'dependency-check.sh --project "DevSecOps-App" --scan .'

                echo "Etape 6 - Secret Scan : Détection de credentials en dur avec TruffleHog..."
                sh 'trufflehog git file://. --only-verified'
            }
        }

        // ==========================================
        // PHASE CONTAINERISATION (Étapes 7, 8)
        // ==========================================
        stage('Phase Containerisation') {
            steps {
                echo "Etape 7 - Docker Build : Construction de l'image Docker..."
                sh "docker build -t ${IMAGE_NAME} ."

                echo "Etape 8 - Container Scan : Scan des CVE de l'image avec Trivy..."
                // Le flag --exit-code 1 permet de bloquer le pipeline en cas de faille critique (Security Gate)
                sh "trivy image --exit-code 1 --severity CRITICAL ${IMAGE_NAME}"
            }
        }

        // ==========================================
        // PHASE DÉPLOIEMENT ET TESTS DYNAMIQUES (Étapes 9, 10)
        // ==========================================
        stage('Phase Deploiement et Tests Dynamiques') {
            steps {
                echo "Etape 9 - Deploy Staging : Déploiement dans l'environnement de test..."
                // Nettoyage d'un ancien conteneur de test s'il existe
                sh "docker rm -f ${CONTAINER_NAME} || true"
                // Lancement du nouveau conteneur sur le port d'écoute de l'app (ex: 3000)
                sh "docker run -d -p 3000:3000 --name ${CONTAINER_NAME} ${IMAGE_NAME}"
                sh "sleep 10" // Temps d'attente pour que l'application démarre proprement

                echo "Etape 10 - DAST : Tests dynamiques avec OWASP ZAP..."
                script {
                    try {
                        // On lance le scan DAST contre l'environnement de Staging fraîchement déployé
                        sh "zap-baseline.py -t http://localhost:3000"
                    } finally {
                        // Nettoyage automatique indispensable du conteneur de staging après les tests
                        echo "Nettoyage de l'environnement de Staging..."
                        sh "docker stop ${CONTAINER_NAME} && docker rm ${CONTAINER_NAME}"
                    }
                }
            }
        }

        // ==========================================
        // SECURITY GATE ET DÉCISIONS (Validation manuelle / Étape 11)
        // ==========================================
        stage('Validation Manuelle Production ?') {
            steps {
                // Interruption visuelle dans Jenkins pour approbation humaine
                input message: "Voulez-vous approuver le déploiement en Production ?", ok: "Approuver"
            }
        }

        stage('Etape 11 - Deploy Production') {
            steps {
                echo "Application approuvée ! Déploiement final en Production avec succès."
                // Exemple de commande finale : sh "docker run -d -p 80:3000 --name app-prod ${IMAGE_NAME}"
            }
        }
    }

    post {
        failure {
            echo "[OUI - BLOQUÉ] Vulnérabilités critiques détectées ou échec technique. Pipeline stoppé."
        }
        aborted {
            echo "[REFUSÉE] Déploiement annulé. Retour en staging."
        }
        success {
            echo "[NON - VALIDÉ / APPROUVÉE] Pipeline DevSecOps complété avec succès !"
        }
    }
}

