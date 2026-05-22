import uasyncio as asyncio
import usocket as socket
import ujson
from machine import UART, Pin

# Configuración de hardware
UART_TX_PIN = 17  # GPIO 17 para TX al Arduino Nano
LED_PIN = 2       # GPIO 2 para LED de status
BAUDRATE = 9600   # Velocidad de comunicación UART

# Inicializar UART y LED
uart = UART(2, tx=Pin(UART_TX_PIN), rx=Pin(16), baudrate=BAUDRATE)
led = Pin(LED_PIN, Pin.OUT)
led.value(1)  # Encender LED al inicio

# Telemetría: ángulo actual leído desde Arduino (en grados)
current_angle = 0

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


async def uart_reader_task():
    """Lee continuamente el UART y actualiza la variable global `current_angle` cuando llega 'ANG:<valor>\n'."""
    global current_angle
    while True:
        try:
            await asyncio.sleep_ms(20)
            if uart.any():
                line = uart.readline()
                if not line:
                    continue
                try:
                    s = line.decode('utf-8').strip()
                except Exception:
                    continue
                if s.startswith('ANG:'):
                    try:
                        val = int(s[4:])
                        current_angle = val
                    except Exception:
                        pass
        except Exception as e:
            print('uart_reader_task error', e)

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
        <div style="display:flex;flex-direction:column;align-items:center;gap:12px;">
            <div class="status" id="status">Listo</div>
            <div class="telemetry" style="margin-top:10px;width:100%;background:#1b1b1b;border:1px solid #333;padding:12px;border-radius:8px;">
                <div style="display:flex;align-items:center;gap:12px;justify-content:center;flex-direction:column;">
                    <svg id="gauge" width="220" height="220" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stop-color="#ff9800" />
                                <stop offset="100%" stop-color="#f44336" />
                            </linearGradient>
                        </defs>
                        <circle cx="100" cy="100" r="88" fill="#121212" stroke="#333" stroke-width="3" />
                        <!-- ticks 0..360 every 30deg -->
                        <g transform="translate(100,100)">
                        </g>
                        <!-- Needle group centered at 100,100 -->
                        <g transform="translate(100,100)">
                            <line id="needle" x1="0" y1="0" x2="0" y2="-70" stroke="url(#grad)" stroke-width="6" stroke-linecap="round" style="transform-box: fill-box; transform-origin: center center; transition: transform 0.18s ease-out;" />
                            <circle cx="0" cy="0" r="6" fill="#fff" />
                        </g>
                    </svg>
                    <div id="angleLabel" style="color:#fff;font-size:20px;font-weight:600;">Orientación de la Pluma: 0°</div>
                </div>
            </div>
        </div>
    </div>
    <script>
        let currentNeedleAngle = 0;

        function normalizeAngle(angle) {
            return ((angle % 360) + 360) % 360;
        }

        function rotateNeedle(targetAngle) {
            const normalized = normalizeAngle(targetAngle);
            const diff = ((normalized - currentNeedleAngle + 540) % 360) - 180;
            currentNeedleAngle = normalizeAngle(currentNeedleAngle + diff);
            const needle = document.getElementById('needle');
            if (needle) {
                needle.style.transform = 'rotate(' + currentNeedleAngle + 'deg)';
            }
        }

        async function sendCommand(cmd) {
            try {
                const response = await fetch(`/control?cmd=${cmd}`);
                if (response.ok) {
                    document.getElementById('status').textContent = `Comando enviado: ${cmd}`;
                } else {
                    document.getElementById('status').textContent = `Error al enviar comando: ${cmd}`;
                }
            } catch (error) {
                document.getElementById('status').textContent = 'Error de comunicación';
            }
        }

        // Telemetría: consultar ángulo cada 200ms
        async function fetchAngle() {
            try {
                const resp = await fetch('/telemetry');
                if (!resp.ok) return;
                const data = await resp.json();
                const angle = normalizeAngle(data.angle);
                const label = document.getElementById('angleLabel');
                if (label) label.textContent = 'Orientación de la Pluma: ' + angle + '°';
                rotateNeedle(angle);
            } catch (e) {
                // ignore
            }
        }

        fetchAngle();
        setInterval(fetchAngle, 200);
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
        elif request_str.startswith('GET /telemetry'):
            # Endpoint de telemetría: devolver ángulo actual en JSON
            response = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n" + ujson.dumps({"angle": current_angle})
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
    # Iniciar tarea que lee UART continuamente
    try:
        asyncio.create_task(uart_reader_task())
    except Exception:
        # compatibilidad con versiones antiguas de uasyncio
        asyncio.ensure_future(uart_reader_task())

    server = await asyncio.start_server(handle_client, '0.0.0.0', 80)
    print("Servidor web asíncrono iniciado en puerto 80")
    led.value(0)  # Apagar LED cuando servidor esté listo (opcional)
    await server.wait_closed()

# Ejecutar el servidor
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nServidor web detenido desde el teclado.")