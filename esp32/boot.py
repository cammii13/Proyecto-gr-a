import network
import time
import machine

# Configuración de WiFi
SSID = 'your_ssid'  # Reemplaza con tu SSID
PASSWORD = 'your_password'  # Reemplaza con tu contraseña

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

# Ejecutar conexión WiFi al inicio
connect_wifi(SSID, PASSWORD)