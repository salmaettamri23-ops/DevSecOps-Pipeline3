import subprocess
import sys


def test_run_sca_scan():
    print("\n--- [SCA] Vérification des vulnérabilités dans vos dépendances (OWASP) ---")

    # Exécution du scan de dépendances
    result = subprocess.run(["pip-audit", "-r", "requirements.txt"], capture_output=True, text=True)
    print(result.stdout)

    if result.returncode != 0:
        print("[ALERTE] Dépendances vulnérables détectées ! Pipeline bloqué.")
        sys.exit(1)
    else:
        print("[SUCCÈS] Aucune faille trouvée dans les dépendances.")


if __name__ == "__main__":
    test_run_sca_scan()
