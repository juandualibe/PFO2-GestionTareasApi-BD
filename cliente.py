import requests

# Definimos la URL base donde está escuchando nuestro servidor (localhost, puerto 5000)
BASE_URL = "http://localhost:5000"

# ─────────────────────────────────────────────
# Funciones
# ─────────────────────────────────────────────

def registrar_usuario():
    """ Envía una solicitud de registro al servidor """
    print("\n── Registro de Usuario ──")
    # Pedimos los datos al usuario por consola
    usuario   = input("Nombre de usuario: ").strip()
    password  = input("Contraseña: ").strip()

    try:
        # El cliente inicia la comunicación enviando un POST con los datos en formato JSON
        respuesta = requests.post(
            f"{BASE_URL}/registro",
            json={"usuario": usuario, "contraseña": password}
        )
        datos = respuesta.json() # Interpretamos la respuesta del servidor
        
        # Verificamos el código de estado (201 para creación exitosa)
        if respuesta.status_code == 201:
            print(f"{datos['mensaje']}")
        else:
            print(f"Error: {datos['error']}")
            
    except requests.exceptions.ConnectionError:
        # Manejamos errores de red o si el servidor está apagado
        print("No se pudo conectar al servidor. ¿Está corriendo servidor.py?")


def iniciar_sesion():
    """ Envía una solicitud de login para validar credenciales """
    print("\n── Inicio de Sesión ──")
    usuario  = input("Nombre de usuario: ").strip()
    password = input("Contraseña: ").strip()

    try:
        # Solicitamos al servidor que verifique las credenciales
        respuesta = requests.post(
            f"{BASE_URL}/login",
            json={"usuario": usuario, "contraseña": password}
        )
        datos = respuesta.json()
        
        # El servidor responde 200 si el login es correcto
        if respuesta.status_code == 200:
            print(f"{datos['mensaje']}")
        else:
            print(f"Error: {datos['error']}")
            
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar al servidor. ¿Está corriendo servidor.py?")


def ver_bienvenida():
    """ Realiza una petición GET para verificar el estado de la API """
    try:
        # Hacemos una solicitud GET a la ruta de tareas
        respuesta = requests.get(f"{BASE_URL}/tareas")
        if respuesta.status_code == 200:
            print("\nServidor respondió correctamente en GET /tareas")
            print("   Abrí http://localhost:5000/tareas en tu navegador para ver la página.")
        else:
            print(f"Error inesperado: {respuesta.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar al servidor. ¿Está corriendo servidor.py?")


# ─────────────────────────────────────────────
# Menú principal (Interfaz de Usuario)
# ─────────────────────────────────────────────

def menu():
    """ Mantiene al cliente en ejecución permitiendo elegir opciones """
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
# Arranque del proceso del cliente
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # Iniciamos el bucle del menú
    menu()