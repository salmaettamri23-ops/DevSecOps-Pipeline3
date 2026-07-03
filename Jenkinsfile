pipeline {
    agent any

    // Cette section indique à Jenkins de charger automatiquement Node.js et npm
    tools {
        nodejs 'NodeJS' // 'NodeJS' doit correspondre au nom configuré dans vos outils Jenkins
    }

    environment {
        IMAGE_NAME = "mon-app-devsecops:latest"
        CONTAINER_NAME = "app-staging-test"
        SONAR_SERVER_NAME = "SonarQube-Server"
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
                sh "trivy image --exit-code 1 --severity CRITICAL ${IMAGE_NAME}"
            }
        }

        // ==========================================
        // PHASE DÉPLOIEMENT ET TESTS DYNAMIQUES (Étapes 9, 10)
        // ==========================================
        stage('Phase Deploiement et Tests Dynamiques') {
            steps {
                echo "Etape 9 - Deploy Staging : Déploiement dans l'environnement de test..."
                sh "docker rm -f ${CONTAINER_NAME} || true"
                sh "docker run -d -p 3000:3000 --name ${CONTAINER_NAME} ${IMAGE_NAME}"
                sh "sleep 10"

                echo "Etape 10 - DAST : Tests dynamiques avec OWASP ZAP..."
                script {
                    try {
                        sh "zap-baseline.py -t http://localhost:3000"
                    } finally {
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
                input message: "Voulez-vous approuver le déploiement en Production ?", ok: "Approuver"
            }
        }

        stage('Etape 11 - Deploy Production') {
            steps {
                echo "Application approuvée ! Déploiement final en Production avec succès."
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
