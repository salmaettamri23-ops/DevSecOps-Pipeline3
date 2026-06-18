from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3

app = Flask(__name__)


# --- CONFIGURATION DE LA BASE DE DONNÉES ---
def init_db():
    """Crée la table des tâches si elle n'existe pas déjà."""
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# --- DESIGN DE L'INTERFACE (HTML/CSS) ---
# Une page web propre pour afficher et ajouter des tâches
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>PFE - Gestionnaire de Tâches SecOps</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; margin: 40px; }
        .container { max-width: 500px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); }
        h2 { color: #333; }
        input[type="text"] { width: 70%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
        input[type="submit"] { padding: 10px 15px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; }
        ul { list-style-type: none; padding: 0; }
        li { padding: 10px; background: #eee; margin-bottom: 5px; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Ma Liste de Tâches Sécurisée</h2>
        <form action="/add" method="POST">
            <input type="text" name="task_title" placeholder="Nouvelle tâche..." required>
            <input type="submit" value="Ajouter">
        </form>
        <h3>Tâches en cours :</h3>
        <ul>
            {% for task in tasks %}
                <li>{{ task[1] }}</li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""


# --- ROUTES DE L'APPLICATION ---

@app.route('/')
def index():
    """Route principale : lit les tâches dans la base et les affiche."""
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    all_tasks = cursor.fetchall()
    conn.close()

    # On envoie les tâches au modèle HTML pour l'affichage
    return render_template_string(HTML_TEMPLATE, tasks=all_tasks)


@app.route('/add', methods=['POST'])
def add_task():
    """Route pour ajouter une nouvelle tâche."""
    title = request.form.get('task_title')

    if title:
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()

        # SÉCURITÉ : Utilisation d'une requête préparée pour éviter les injections SQL
        cursor.execute("INSERT INTO tasks (title) VALUES (?)", (title,))

        conn.commit()
        conn.close()

    return redirect(url_for('index'))


if __name__ == '__main__':
    # Initialise la base de données au démarrage
    init_db()
    # Lance l'application sur le port 5000
    app.run(host='0.0.0.0', port=5000)
