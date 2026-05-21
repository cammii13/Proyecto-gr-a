import uasyncio as asyncio
import usocket as socket
import ujson
from machine import UART, Pin

# Configuración de hardware
UART_TX_PIN = 17  # GPIO 17 para TX al Arduino Nano
LED_PIN = 2       # GPIO 2 para LED de status
BAUDRATE = 9600   # Velocidad de comunicación UART

# Inicializar UART y LED
uart = UART(2, tx=Pin(UART_TX_PIN), rx=Pin(16), baudrate=BAUDRATE)  # RX no usado, pero definido
led = Pin(LED_PIN, Pin.OUT)
led.value(1)  # Encender LED al inicio

# Comandos según estándar OpenSpec (ejemplo simplificado)
COMMANDS = {
    'car_left': 'CL',    # Carro izquierda
    'car_right': 'CR',   # Carro derecha
    'elev_up': 'EU',     # Elevación arriba
    'elev_down': 'ED',   # Elevación abajo
    'giro_left': 'GL',   # Giro izquierda
    'giro_right': 'GR',  # Giro derecha
    'stop': 'S'          # Parar todos los motores
}

def send_to_uart(cmd):
    """
    Envía comando UART al Arduino Nano.
    """
    if cmd in COMMANDS:
        message = COMMANDS[cmd] + '\n'
        uart.write(message.encode())
        print(f"Comando enviado: {cmd}")
    else:
        print(f"Comando desconocido: {cmd}")

def parse_cmd(request_str):
    """
    Parsea el parámetro cmd de la URL.
    """
    if 'cmd=' in request_str:
        start = request_str.find('cmd=') + 4
        end = request_str.find(' ', start)
        return request_str[start:end]
    return None

def get_html():
    """
    Genera el HTML de la interfaz web.
    """
    html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Control Grúa Torre</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background-color: #121212; color: #ffffff; margin: 0; padding: 20px; }
        .container { max-width: 400px; margin: auto; }
        .control-group { margin: 20px 0; }
        .control-group h2 { margin-bottom: 10px; color: #ffffff; }
        .button-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
        button { padding: 20px; font-size: 18px; border: none; border-radius: 10px; background-color: #333333; color: #ffffff; cursor: pointer; transition: background-color 0.3s; }
        button:hover { background-color: #555555; }
        button:active { background-color: #777777; }
        .stop-button { background-color: #dc3545; grid-column: span 2; }
        .stop-button:hover { background-color: #c82333; }
        .status { margin-top: 20px; padding: 10px; background-color: #1e1e1e; border: 1px solid #333333; border-radius: 5px; color: #ffffff; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Control de Grúa Torre</h1>
        <div class="control-group">
            <h2>Carro</h2>
            <div class="button-grid">
                <button onclick="sendCommand('car_left')">Izquierda</button>
                <button onclick="sendCommand('car_right')">Derecha</button>
            </div>
        </div>
        <div class="control-group">
            <h2>Elevación</h2>
            <div class="button-grid">
                <button onclick="sendCommand('elev_up')">Arriba</button>
                <button onclick="sendCommand('elev_down')">Abajo</button>
            </div>
        </div>
        <div class="control-group">
            <h2>Giro</h2>
            <div class="button-grid">
                <button onclick="sendCommand('giro_left')">Izquierda</button>
                <button onclick="sendCommand('giro_right')">Derecha</button>
            </div>
        </div>
        <div class="control-group">
            <button class="stop-button" onclick="sendCommand('stop')">PARAR</button>
        </div>
        <div class="status" id="status">Listo</div>
    </div>
    <script>
        async function sendCommand(cmd) {
            try {
                const response = await fetch(`/control?cmd=${cmd}`);
                const data = await response.json();
                document.getElementById('status').textContent = `Comando enviado: ${cmd}`;
            } catch (error) {
                document.getElementById('status').textContent = 'Error al enviar comando';
            }
        }
    </script>
</body>
</html>
    """
    return html

async def handle_client(reader, writer):
    """
    Maneja las conexiones HTTP entrantes.
    """
    try:
        request = await reader.read(1024)
        request_str = request.decode('utf-8')

        if request_str.startswith('GET / '):
            # Servir página principal
            html = get_html()
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{html}"
        elif request_str.startswith('GET /control?'):
            # Procesar comando
            cmd = parse_cmd(request_str)
            if cmd:
                send_to_uart(cmd)
                response = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n" + ujson.dumps({"status": "ok"})
            else:
                response = "HTTP/1.1 400 Bad Request\r\n\r\n"
        else:
            # Página no encontrada
            response = "HTTP/1.1 404 Not Found\r\n\r\n"

        await writer.awrite(response.encode('utf-8'))
    except Exception as e:
        print(f"Error en handle_client: {e}")
    finally:
        await writer.aclose()

async def main():
    """
    Función principal: inicia el servidor web.
    """
    server = await asyncio.start_server(handle_client, '0.0.0.0', 80)
    print("Servidor web asíncrono iniciado en puerto 80")
    led.value(0)  # Apagar LED cuando servidor esté listo (opcional)
    await server.wait_closed()

# Ejecutar el servidor
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nServidor web detenido desde el teclado.")