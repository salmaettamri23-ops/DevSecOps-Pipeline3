import sys
import requests

# L'URL sur laquelle tourne votre application
BASE_URL = "http://127.0.0.1:5000"


def test_security_routes():
    print("\n--- [DAST] Simulation d'attaques dynamiques (OWASP ZAP) ---")
    payload = "<script>alert('hack')</script>"

    try:
        # Envoi d'une requête test pour voir si l'application est vulnérable au XSS
        response = requests.get(f"{BASE_URL}/", params={"q": payload})
        if payload in response.text:
            print("[ALERTE] Faille de sécurité potentielle détectée !")
            return False
        print("[SUCCÈS] L'application réagit correctement aux attaques de test.")
        return True
    except requests.exceptions.ConnectionError:
        print(f"[ERREUR] Impossible de contacter l'application sur {BASE_URL}. Vérifiez qu'elle a démarré.")
        return False


if __name__ == "__main__":
    if not test_security_routes():
        sys.exit(1)
