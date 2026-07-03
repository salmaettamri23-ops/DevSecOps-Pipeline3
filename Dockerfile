# 1. Utiliser une image de base Python officielle et légère
FROM python:3.11-slim

# 2. Définir le dossier de travail à l'intérieur du conteneur
WORKDIR /app

# 3. Copier le fichier des dépendances dans le conteneur
COPY requirements.txt .

# 4. Installer les dépendances de l'application
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copier le reste du code de l'application (app.py, etc.)
COPY . .

# 6. Exposer le port sur lequel votre application écoute (ex: 5000 pour Flask)
EXPOSE 5000

# 7. Définir la commande par défaut pour lancer l'application
CMD ["python", "app.py"]

