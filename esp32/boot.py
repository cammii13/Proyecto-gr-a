import network
import time
import machine
import sys
import uselect

# Configuración de WiFi
SSID = 'your_ssid'  # Reemplaza con tu SSID
PASSWORD = 'your_password'  # Reemplaza con tu contraseña

def menu_inicio(timeout_segundos=5):
    """
    Muestra un menú en la terminal. Avanza automáticamente si no hay respuesta.
    """
    print("\n" + "="*40)
    print("      SISTEMA DE CONTROL - GRÚA TORRE")
    print("="*40)
    print("1. Iniciar sistema normalmente (Modo Ejecución)")
    print("2. Detener en modo programación (Liberar REPL)")
    print(f"Selecciona una opción (Avanza a opción 1 en {timeout_segundos}s)...")
    
    # Configurar la terminal para escuchar la entrada del usuario sin bloquear
    poller = uselect.poll()
    poller.register(sys.stdin, uselect.POLLIN)
    
    tiempo_inicio = time.time()
    while (time.time() - tiempo_inicio) < timeout_segundos:
        # Revisar si hay datos en la terminal (espera hasta 100ms por ciclo)
        if poller.poll(100):
            caracter = sys.stdin.read(1)
            if caracter == '1':
                print("\n-> Opción 1 seleccionada. Iniciando...")
                return True
            elif caracter == '2':
                print("\n-> Opción 2 seleccionada. Modo programación activo.")
                print("Consola REPL liberada. Puedes subir o modificar archivos.")
                return False
    
    # Si se agota el tiempo sin respuesta, asumimos que está corriendo en la grúa de forma autónoma
    print("\n-> Tiempo de espera agotado. Iniciando de forma automática...")
    return True

def connect_wifi(ssid, password, max_attempts=10):
    """
    Función para conectar a WiFi con manejo de errores y reintentos.
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    print("Conectando a WiFi...")
    attempts = 0
    while attempts < max_attempts:
        try:
            wlan.connect(ssid, password)
            # Esperar hasta 10 segundos por conexión
            timeout = 10
            while not wlan.isconnected() and timeout > 0:
                time.sleep(1)
                timeout -= 1
                print(".", end="")

            if wlan.isconnected():
                print("\nConectado a WiFi. IP:", wlan.ifconfig()[0])
                return True
            else:
                print("\nFallo en conexión, reintentando...")
                attempts += 1
                time.sleep(2)
        except Exception as e:
            print(f"Error al conectar: {e}")
            attempts += 1
            time.sleep(2)

    print("No se pudo conectar a WiFi después de varios intentos.")
    # Reiniciar el dispositivo si falla
    machine.reset()
    return False

# --- FLUJO DE INICIO ---

# Ejecutamos el menú ANTES de conectar al WiFi o cargar el main
if menu_inicio(timeout_segundos=5):
    # Si elige 1 o se agota el tiempo, conecta a WiFi y avanza a main.py
    connect_wifi(SSID, PASSWORD)
else:
    # Si elige 2, forzamos la detención del script del sistema operativo
    # Esto evita que MicroPython salte automáticamente a ejecutar el main.py
    sys.exit()