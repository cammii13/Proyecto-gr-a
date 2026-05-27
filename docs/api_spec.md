# API Spec (OpenSpec v1.1)

Este documento centraliza la especificación técnica del API expuesto por el ESP32 y el protocolo UART bidireccional entre el ESP32 y el Arduino Nano.

## Endpoints HTTP (ESP32 - `main.py`)

| Endpoint | Método | Descripción | Parámetros | Respuesta |
|---|---:|---|---|---|
| `/` | GET | Interfaz web HTML principal | — | HTML (200)
| `/telemetry` | GET | Obtiene el estado actual de la grúa | — | JSON `{ "angle": <int>, "mode": "web"\|"manual" }` (200)
| `/control` | GET | Envía comandos de movimiento o cambio de modo | `cmd` (string) — valores: `car_left`, `car_right`, `elev_up`, `elev_down`, `giro_left`, `giro_right`, `stop`, `mode_manual`, `mode_web` | JSON `{ "status": "ok" }` (200) o 400 si falta `cmd`

### Comportamiento del API Web:
- El cliente web sondea periódicamente `/telemetry` (cada 200 ms) para mantener sincronizados el ángulo de rotación de la pluma y la posición del interruptor de modo.
- El endpoint `/control` traduce el parámetro `cmd` al código UART correspondiente y lo envía inmediatamente al Arduino.

---

## Protocolo de Mensajería UART (Conexión Serie)

- **Parámetros del enlace físico:** 9600 bps, 8N1.
- **Formato de trama:** Texto ASCII plano terminado en un carácter de nueva línea (`\n`).

### Comandos de Entrada (ESP32 → Arduino Nano)

| Código | Comando lógico | Descripción | Actuador / Estado afectado |
|---|---|---|---|
| `CL` | `car_left` | Mover carro a la izquierda | Motor DC Carro |
| `CR` | `car_right` | Mover carro a la derecha | Motor DC Carro |
| `EU` | `elev_up` | Subir gancho | Motor DC Elevación |
| `ED` | `elev_down` | Bajar gancho | Motor DC Elevación |
| `GL` | `giro_left` | Rotar pluma a la izquierda | Motor DC Giro |
| `GR` | `giro_right` | Rotar pluma a la derecha | Motor DC Giro |
| `S`  | `stop` | Parar todos los movimientos | Todos los motores |
| `MM` | `mode_manual` | Activar modo manual (Joysticks) | Inhabilita control UART de movimiento |
| `MW` | `mode_web` | Activar modo web | Ignora lecturas de Joysticks analógicos |

### Reportes de Salida (Arduino Nano → ESP32)

| Formato de Mensaje | Descripción | Cuándo se envía |
|---|---|---|
| `ANG:<valor_entero>\n` | Reporta el ángulo de rotación estimado de la pluma (rango `0` a `359`). | Periódicamente en cada cambio de posición estimado. |
| `MOD:MANUAL\n` | Confirma el cambio a modo de control manual por joysticks. | Inmediatamente después de conmutar por botón D6 o recibir `MM`. |
| `MOD:WEB\n` | Confirma el cambio a modo de control por interfaz web. | Inmediatamente después de conmutar por botón D6 o recibir `MW`. |

### Timeout de Seguridad
- En **Modo Web**, si el Arduino no recibe ningún comando válido por UART durante 2000 ms, invocará internamente `stopAllMotors()` para evitar desplazamientos por pérdida de conexión WiFi o caída del servidor web.
