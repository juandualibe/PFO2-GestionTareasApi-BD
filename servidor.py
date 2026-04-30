from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3


app = Flask(__name__)

DB_PATH = "tareas.db"

# ─────────────────────────────────────────────
# Inicialización de la base de datos
# ─────────────────────────────────────────────

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario  TEXT    NOT NULL UNIQUE,
                password TEXT    NOT NULL
            )
        """)
        conn.commit()

# ─────────────────────────────────────────────
# Endpoint: POST /registro
# ─────────────────────────────────────────────

@app.route("/registro", methods=["POST"])
def registro():
    datos = request.get_json()

    if not datos or "usuario" not in datos or "contraseña" not in datos:
        return jsonify({"error": "Faltan campos: 'usuario' y 'contraseña'"}), 400

    usuario   = datos["usuario"].strip()
    password  = datos["contraseña"].strip()

    if not usuario or not password:
        return jsonify({"error": "Los campos no pueden estar vacíos"}), 400

    password_hash = generate_password_hash(password)

    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO usuarios (usuario, password) VALUES (?, ?)",
                (usuario, password_hash)
            )
            conn.commit()
        return jsonify({"mensaje": f"Usuario '{usuario}' registrado exitosamente"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": f"El usuario '{usuario}' ya existe"}), 409

# ─────────────────────────────────────────────
# Endpoint: POST /login
# ─────────────────────────────────────────────

@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json()

    if not datos or "usuario" not in datos or "contraseña" not in datos:
        return jsonify({"error": "Faltan campos: 'usuario' y 'contraseña'"}), 400

    usuario  = datos["usuario"].strip()
    password = datos["contraseña"].strip()

    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT password FROM usuarios WHERE usuario = ?", (usuario,)
        ).fetchone()

    if row is None or not check_password_hash(row[0], password):
        return jsonify({"error": "Credenciales incorrectas"}), 401

    return jsonify({"mensaje": f"Bienvenido, {usuario}!"}), 200

# ─────────────────────────────────────────────
# Endpoint: GET /tareas
# ─────────────────────────────────────────────

@app.route("/tareas", methods=["GET"])
def tareas():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Gestor de Tareas</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f0f4f8;
            }
            .card {
                background: white;
                padding: 2rem 3rem;
                border-radius: 12px;
                box-shadow: 0 4px 16px rgba(0,0,0,0.1);
                text-align: center;
            }
            h1 { color: #2d6a4f; }
            p  { color: #555; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Sistema de Gestión de Tareas</h1>
            <p>El servidor está funcionando correctamente.</p>
            <p>Usá los endpoints <strong>/registro</strong> y <strong>/login</strong> para comenzar.</p>
        </div>
    </body>
    </html>
    """, 200

# ─────────────────────────────────────────────
# Arranque
# ─────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    print("Servidor iniciado en http://localhost:5000")
    app.run(debug=True)