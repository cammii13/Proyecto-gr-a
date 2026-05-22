# API Spec (OpenSpec v1.0)

Este documento centraliza la especificación técnica del API expuesto por el ESP32 y el protocolo UART entre ESP32 y Arduino.

## Endpoints HTTP (ESP32 - `main.py`)

| Endpoint | Método | Descripción | Parámetros | Respuesta |
|---|---:|---|---|---|
| `/` | GET | Página principal (interfaz web HTML) | — | HTML (200)
| `/control` | GET | Envía un comando de control al Arduino vía UART | `cmd` (string) — valores: `car_left`, `car_right`, `elev_up`, `elev_down`, `giro_left`, `giro_right`, `stop` | JSON `{ "status": "ok" }` (200) o 400 si falta `cmd`

Descripción de comportamiento:
- La página raíz sirve HTML/CSS/JS responsive en tema oscuro.
- El endpoint `/control` espera una petición `GET` con parámetro `cmd` y, en caso válido, mapea el comando a un código corto (OpenSpec) y lo escribe al UART.
- Comunicaciones web se hacen desde el front-end mediante `fetch()` para evitar recargas.

## Protocolo de Mensajería UART (Arduino: `grúa_arduino.ino`)

Formato de mensaje:
- Mensaje ASCII terminando en `\n`.
- Cada comando es un código de 1–2 caracteres seguido de nueva línea: `<CODE>\n`.

Tabla de comandos:

| Código | Comando lógico | Descripción | Motor afectado |
|---|---|---|---|
| `CL` | `car_left` | Mover carro a la izquierda | Motor DC Carro |
| `CR` | `car_right` | Mover carro a la derecha | Motor DC Carro |
| `EU` | `elev_up` | Subir elevación | Motor DC Elevación |
| `ED` | `elev_down` | Bajar elevación | Motor DC Elevación |
| `GL` | `giro_left` | Giro a la izquierda (stepper) | Motor Paso (Nema 17) |
| `GR` | `giro_right` | Giro a la derecha (stepper) | Motor Paso (Nema 17) |
| `S`  | `stop` | Parar todos los motores | Todos |

Parámetros de enlace físico y timing:
- **Baudrate**: 9600 bps
- **Formato**: ASCII + `\n` como terminador
- **Timeout de seguridad**: si no se reciben comandos durante 2000 ms, el Arduino ejecuta `stopAllMotors()`.
- **Conexión RX/TX**: ESP32 TX (GPIO 17) → Arduino RX (D0). (Nota: `main.py` inicializa UART con `tx=17`.)

Notas de validación:
- El Arduino ignora comandos no reconocidos; sólo procesa los códigos listados.
- Se recomienda verificar continuidad y nivel lógico de la conexión TX/RX y la alimentación antes de probar.
