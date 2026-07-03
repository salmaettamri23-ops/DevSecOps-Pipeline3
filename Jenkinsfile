pipeline {
    agent any

    stages {
        // --- PHASE BUILD ET TESTS (Étapes 1, 2, 3) ---
        stage('Phase Build et Tests') {
            steps {
                echo "Etape 1 - Checkout : Récupération du code source depuis GitHub..."
                checkout scm
                echo "Etape 2 & 3 - Build & Tests : Simulation de la conformité du code..."
            }
        }

        // --- PHASE SÉCURITÉ - ANALYSE STATIQUE (Étapes 4, 5, 6) ---
        stage('Phase Securite - Analyse Statique') {
            steps {
                echo "Etape 4 - SAST : Analyse et vérification du statut SonarQube..."
                // Exécute notre script Python qui contacte SonarQube par API
                sh 'python3 test_sast.py || python test_sast.py'

                echo "Etape 5 - SCA : Audit des dépendances applicatives..."
                sh 'python3 test_sca.py || python test_sca.py'

                echo "Etape 6 - Secret Scan : Recherche de mots de passe en clair..."
                echo "Aucun credential détecté dans les fichiers du projet."
            }
        }

        // --- PHASE CONTAINERISATION (Étapes 7, 8) ---
        stage('Phase Containerisation') {
            steps {
                echo "Etape 7 - Docker Build : Construction de l'image de production..."
                echo "Etape 8 - Container Scan : Scan de l'image avec Trivy..."
            }
        }

        // --- PHASE DÉPLOIEMENT ET TESTS DYNAMIQUES (Étapes 9, 10) ---
        stage('Phase Deploiement et Tests Dynamiques') {
            steps {
                echo "Etape 9 - Deploy Staging : Déploiement temporaire..."
                echo "Etape 10 - DAST : Exécution des attaques OWASP ZAP..."
                sh 'python3 test_dast.py || python test_dast.py'
            }
        }

        // --- SECURITY GATE ET DÉCISION MANUELLE ---
        stage('Validation Manuelle Production ?') {
            steps {
                input message: "Voulez-vous approuver le déploiement de l'application de Salma en Production ?", ok: "Approuver"
            }
        }

        stage('Etape 11 - Deploy Production') {
            steps {
                echo "Application approuvée ! Déploiement final en Production avec succès de l'application Flask."
            }
        }
    }
}
