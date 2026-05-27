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

# Telemetría
current_angle = 0
control_mode = "web"  # "web" o "manual"

# Comandos según estándar OpenSpec (ejemplo simplificado)
COMMANDS = {
    'car_left': 'CL',    # Carro izquierda
    'car_right': 'CR',   # Carro derecha
    'elev_up': 'EU',     # Elevación arriba
    'elev_down': 'ED',   # Elevación abajo
    'giro_left': 'GL',   # Giro izquierda
    'giro_right': 'GR',  # Giro derecha
    'stop': 'S',         # Parar todos los motores
    'mode_manual': 'MM', # Activar modo manual (joysticks)
    'mode_web': 'MW'     # Activar modo web
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
    """Lee continuamente el UART y actualiza el ángulo y modo."""
    global current_angle, control_mode
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
                elif s == 'MOD:MANUAL':
                    control_mode = "manual"
                    print("Modo de control actualizado: MANUAL")
                elif s == 'MOD:WEB':
                    control_mode = "web"
                    print("Modo de control actualizado: WEB")
        except Exception as e:
            print('uart_reader_task error', e)

def get_html():
    """
    Lee el archivo index.html del sistema de archivos local.
    """
    try:
        with open('index.html', 'r') as f:
            return f.read()
    except Exception as e:
        print("Error al leer index.html:", e)
        return "<html><body><h1>Error 500: Archivo index.html no encontrado en la memoria del dispositivo</h1></body></html>"


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
            # Endpoint de telemetría: devolver ángulo y modo actual en JSON
            response = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n" + ujson.dumps({"angle": current_angle, "mode": control_mode})
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