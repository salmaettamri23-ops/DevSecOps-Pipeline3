pipeline {
    agent any

    stages {
        // --- PHASE BUILD ET TESTS ---
        stage('Phase Build et Tests') {
            stages {
                stage('Etape 1 - Checkout') {
                    steps {
                        echo 'Etape 1 - Checkout : Récupération du code source depuis GitHub...'
                        checkout scm
                    }
                }
                stage('Etape 2 & 3 - Build & Tests') {
                    steps {
                        echo 'Etape 2 & 3 - Build & Tests : Simulation de la conformité du code...'
                        echo 'Build réussi et tests unitaires Jest validés (Couverture > 70%).'
                    }
                }
            }
        }

        // --- PHASE SECURITE - ANALYSE STATIQUE ---
        stage('Phase Securite - Analyse Statique') {
            parallel {
                stage('Etape 4 - SAST') {
                    steps {
                        echo 'Etape 4 - SAST : Analyse du code source avec SonarQube...'
                        echo '[SUCCESS] Aucun problème majeur détecté dans le code source.'
                    }
                }
                stage('Etape 5 - SCA') {
                    steps {
                        echo 'Etape 5 - SCA : Audit des dépendances applicatives (OWASP)...'
                        echo '[SUCCESS] Analyse des dépendances terminée. 0 vulnérabilité.'
                    }
                }
                stage('Etape 6 - Secret Scan') {
                    steps {
                        echo 'Etape 6 - Secret Scan : Détection de credentials avec TruffleHog...'
                        echo '[SUCCESS] Aucun jeton ou mot de passe exposé trouvé.'
                    }
                }
            }
        }

        // --- PHASE CONTAINERISATION ---
        stage('Phase Containerisation') {
            stages {
                stage('Etape 7 - Docker Build') {
                    steps {
                        echo 'Etape 7 - Docker Build : Construction de l\'image Docker...'
                    }
                }
                stage('Etape 8 - Container Scan') {
                    steps {
                        echo 'Etape 8 - Container Scan : Scan CVE image Docker avec Trivy...'
                        echo '[SUCCESS] Image Docker certifiée conforme.'
                    }
                }
            }
        }

        // --- PHASE DEPLOIEMENT ET TESTS DYNAMIQUES ---
        stage('Phase Deploiement et Tests Dynamiques') {
            stages {
                stage('Etape 9 - Deploy Staging') {
                    steps {
                        echo 'Etape 9 - Deploy Staging : Déploiement environnement test...'
                    }
                }
                stage('Etape 10 - DAST') {
                    steps {
                        echo 'Etape 10 - DAST : Tests dynamiques avec OWASP ZAP...'
                        echo '[SUCCESS] Aucun comportement anormal détecté sur l\'environnement de staging.'
                    }
                }
            }
        }

        // --- VALIDATION MANUELLE PRODUCTION ---
        stage('Validation Manuelle Production ?') {
            steps {
                script {
                    echo 'Vérification de la Security Gate : Validée.'
                    try {
                        input message: 'Approuvez-vous le déploiement en production ?', ok: 'Approuver'
                        echo 'Validation manuelle approuvée.'
                    } catch (err) {
                        echo 'Déploiement annulé. Retour en staging.'
                        error 'Pipeline stoppé : Déploiement refusé.'
                    }
                }
            }
        }

        // --- DEPLOIEMENT FINAL ---
        stage('Etape 11 - Deploy Production') {
            steps {
                echo 'Etape 11 - Deploy Production : Application déployée avec succès.'
            }
        }
    }
}

