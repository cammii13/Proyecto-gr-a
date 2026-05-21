# Proyecto Grúa Torre - Documentación Técnica (OpenSpec v1.0)

## Descripción General

Este proyecto implementa un sistema de control para una grúa torre con dos controladores: un ESP32 para la interfaz web remota y un Arduino Nano para el control de motores. El sistema permite control manual vía joysticks y remoto vía web, utilizando comunicación UART entre los dispositivos.

## Arquitectura del Sistema

La arquitectura se basa en una comunicación serial entre el ESP32 (interfaz web) y el Arduino Nano (control de actuadores). El diagrama simplificado es el siguiente:

```
+----------------+       UART       +-----------------+
|     ESP32      | <--------------> |  Arduino Nano   |
| (Servidor Web) |                  | (Control Motores)|
| - WiFi         |                  | - Motores DC     |
| - HTML/JS      |                  | - Motor Paso     |
| - API REST     |                  | - Joysticks      |
+----------------+                  +-----------------+
         |
         | HTTP
         v
+----------------+
|   Cliente Web  |
| (Navegador)    |
+----------------+
```

- **ESP32**: Gestiona la conexión WiFi, servidor web asíncrono y envío de comandos UART.
- **Arduino Nano**: Recibe comandos UART, controla motores DC (carro y elevación) y motor de pasos (giro), lee joysticks.
- **Comunicación**: UART a 9600 baudios para comandos, HTTP para interfaz web.

## Endpoints de la API

El ESP32 expone una API REST simple para control remoto. La tabla a continuación detalla los endpoints disponibles:

| Endpoint          | Método | Descripción                          | Parámetros                  | Respuesta |
|-------------------|--------|--------------------------------------|-----------------------------|-----------|
| `/control`        | GET    | Envía un comando de control al Arduino | `cmd` (string): comando UART | `{"status": "ok"}` o error |

### Ejemplos de Uso

- Mover carro a la izquierda: `GET /control?cmd=car_left`
- Elevar la grúa: `GET /control?cmd=elev_up`
- Girar a la derecha: `GET /control?cmd=giro_right`
- Parar todos los motores: `GET /control?cmd=stop`

Los comandos se envían vía UART al Arduino Nano sin recargar la página web, utilizando JavaScript Fetch API.

## Protocolo de Mensajería UART

La comunicación UART utiliza mensajes de texto simples terminados en nueva línea (`\n`). Cada comando es un código de 2 letras que indica la acción del motor. El protocolo incluye frenado automático si no se reciben comandos en 2 segundos. La tabla es la siguiente:

| Comando | Descripción              | Motor Afectado |
|---------|--------------------------|----------------|
| `CL`    | Carro izquierda          | Motor DC Carro |
| `CR`    | Carro derecha            | Motor DC Carro |
| `EU`    | Elevación arriba         | Motor DC Elevación |
| `ED`    | Elevación abajo          | Motor DC Elevación |
| `GL`    | Giro izquierda           | Motor Paso Nema 17 |
| `GR`    | Giro derecha             | Motor Paso Nema 17 |
| `S`     | Parar todos los motores  | Todos |

- **Formato**: `<COMANDO>\n`
- **Baudrate**: 9600
- **Dirección**: ESP32 TX (GPIO 17) → Arduino RX (D0)
- **Notas**: Los comandos se procesan en tiempo real. El Arduino combina intenciones de joysticks y comandos remotos. Incluye frenado automático por timeout de 2 segundos.

## Características de Seguridad

- **Frenado Automático**: Si no se reciben comandos en 2 segundos, el Arduino detiene automáticamente todos los motores para prevenir accidentes.
- **Validación de Comandos**: Solo comandos válidos son procesados; comandos desconocidos son ignorados.
- **Interfaz Segura**: La interfaz web requiere conexión WiFi y no expone puertos adicionales.

## Flujo de Inicio del ESP32 (boot.py)

El archivo `boot.py` implementa un menú interactivo que se ejecuta al iniciar el ESP32. Este menú permite elegir entre dos modos:

### Menú de Inicio
```
========================================
      SISTEMA DE CONTROL - GRÚA TORRE
========================================
1. Iniciar sistema normalmente (Modo Ejecución)
2. Detener en modo programación (Liberar REPL)
Selecciona una opción (Avanza a opción 1 en 5s)...
```

- **Opción 1 (o timeout)**: El ESP32 se conecta a WiFi automáticamente y carga el servidor web desde `main.py`.
- **Opción 2**: Detiene la ejecución automática del script y libera la consola REPL de MicroPython para programación interactiva.
- **Timeout**: Si no se selecciona nada en 5 segundos, el sistema avanza automáticamente a la opción 1 (ideal para operación autónoma).

## Servidor Web del ESP32 (main.py)

El archivo `main.py` implementa un servidor web asíncrono que:
- Expone una interfaz HTML interactiva para control remoto de la grúa.
- Recibe comandos desde la web y los envía al Arduino Nano vía UART.
- Implementa control de tres ejes: carro (izquierda/derecha), elevación (arriba/abajo), giro (izquierda/derecha).
- Incluye botón de emergencia (PARAR) que detiene todos los motores instantáneamente.

### Características de la Interfaz Web
- Diseño responsive en tema oscuro (azul #121212).
- Botones de fácil acceso para cada eje de movimiento.
- Feedback visual con cambio de color en botones presionados.
- Mostrador de estado en tiempo real.

## Instrucciones de Instalación

### Requisitos Previos
- ESP32 DevKit V1 con MicroPython instalado.
- Arduino Nano con Arduino IDE.
- Librerías: AccelStepper para Arduino, uasyncio para MicroPython (instalar vía upip si necesario).
- Conexión WiFi disponible.

### Instalación ESP32
1. Conecta el ESP32 a tu PC vía USB.
2. Usa Thonny IDE para subir `boot.py` y `main.py` al dispositivo.
3. Edita `boot.py` con tus credenciales WiFi (SSID y PASSWORD).
4. Reinicia el ESP32:
   - Se mostrará el menú de inicio por 5 segundos.
   - Presiona **1** para inicio normal (o espera al timeout).
   - Presiona **2** si deseas entrar en modo programación (libera REPL).
5. Una vez conectado a WiFi, el servidor web estará disponible en `http://<IP_ESP32>/`.

### Instalación Arduino
1. Abre `arduino/grúa_arduino.ino` en Arduino IDE.
2. Instala la librería AccelStepper desde el gestor de librerías.
3. Verifica y sube el código al Arduino Nano.
4. Conecta pines según requirements.md: STEP (D9), DIR (D10), etc.

### Configuración del Sistema
1. Conecta UART: ESP32 TX (GPIO 17) a Arduino RX (D0).
2. Alimenta ambos dispositivos.
3. Al iniciar, se mostrará el menú en el serial (115200 bauds).
4. Selecciona modo o espera al timeout.
5. Accede a la IP del ESP32 desde un navegador para la interfaz web.
6. Prueba controles remotos y verifica LEDs de status.

### Solución de Problemas
- Si no conecta WiFi, verifica credenciales en `boot.py`.
- Para errores UART, confirma baudrate y conexiones físicas.
- LED en GPIO 2 del ESP32 indica status (encendido = listo).

---

**Versión**: 1.0  
**Fecha**: 11 de mayo de 2026  
**Autor**: Camila Llusca