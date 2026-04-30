import requests
 
BASE_URL = "http://localhost:5000"
 
# ─────────────────────────────────────────────
# Funciones
# ─────────────────────────────────────────────
 
def registrar_usuario():
    print("\n── Registro de Usuario ──")
    usuario   = input("Nombre de usuario: ").strip()
    password  = input("Contraseña: ").strip()
 
    try:
        respuesta = requests.post(
            f"{BASE_URL}/registro",
            json={"usuario": usuario, "contraseña": password}
        )
        datos = respuesta.json()
        if respuesta.status_code == 201:
            print(f"{datos['mensaje']}")
        else:
            print(f"Error: {datos['error']}")
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar al servidor. ¿Está corriendo servidor.py?")
 
 
def iniciar_sesion():
    print("\n── Inicio de Sesión ──")
    usuario  = input("Nombre de usuario: ").strip()
    password = input("Contraseña: ").strip()
 
    try:
        respuesta = requests.post(
            f"{BASE_URL}/login",
            json={"usuario": usuario, "contraseña": password}
        )
        datos = respuesta.json()
        if respuesta.status_code == 200:
            print(f"{datos['mensaje']}")
        else:
            print(f"Error: {datos['error']}")
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar al servidor. ¿Está corriendo servidor.py?")
 
 
def ver_bienvenida():
    try:
        respuesta = requests.get(f"{BASE_URL}/tareas")
        if respuesta.status_code == 200:
            print("\nServidor respondió correctamente en GET /tareas")
            print("   Abrí http://localhost:5000/tareas en tu navegador para ver la página.")
        else:
            print(f"Error inesperado: {respuesta.status_code}")
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar al servidor. ¿Está corriendo servidor.py?")
 
 
# ─────────────────────────────────────────────
# Menú principal
# ─────────────────────────────────────────────
 
def menu():
    while True:
        print("\n")
        print("Sistema de Gestión de Tareas")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Ver página de bienvenida")
        print("4. Salir")
        print("════════════════════════════")
 
        opcion = input("Elegí una opción: ").strip()
 
        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            iniciar_sesion()
        elif opcion == "3":
            ver_bienvenida()
        elif opcion == "4":
            print("\nHasta luego")
            break
        else:
            print("Opción inválida, intentá de nuevo.")
 
 
# ─────────────────────────────────────────────
# Arranque
# ─────────────────────────────────────────────
 
if __name__ == "__main__":
    menu()