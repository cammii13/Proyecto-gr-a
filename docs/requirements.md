# Proyecto Grúa Torre: Requerimientos Técnicos para Generación de Código (v3)

## Contexto del Proyecto

Este documento define las especificaciones técnicas del hardware y software de la grúa torre para posibilitar el control dual (Manual vía Joysticks y Remoto vía Web) mediante comunicación serial bidireccional entre un ESP32 y un Arduino Nano. El movimiento del sistema se realiza con tres motores DC controlados por dos puentes H TB6612FNG.

## 1. Arquitectura de Hardware y Pines

### Controlador A: Arduino Nano (Actuador Principal)
- **Framework:** Arduino / C++
- **Responsabilidad:** Controlar motores DC, leer entradas de joysticks, manejar la conmutación de modo (manual/web) y reportar estimación de telemetría al ESP32.
- **Asignación de Pines:**
  - **Joysticks:**
    - Joystick 1: Eje X (Carro) -> Analógico A0, Eje Y (Giro) -> Analógico A2.
    - Joystick 2: Eje X (Elevación) -> Analógico A1, Pulsador (Botón de Modo) -> Digital D6.
  - **Driver TB6612FNG (1) - Carro y Elevación:**
    - Motor A (Carro): AIN1 (D2), AIN2 (D4), PWMA (D3).
    - Motor B (Elevación): BIN1 (D7), BIN2 (D8), PWMB (D5).
    - STBY -> Habilitado (conectado a VCC 5V).
  - **Driver TB6612FNG (2) - Giro:**
    - Motor C (Giro): CIN1 (D11), CIN2 (D12), PWMC (D9).
    - STBY -> Habilitado (conectado a VCC 5V).
  - **Comunicación Serie:**
    - RX (D0) conectado al TX del ESP32.
    - TX (D1) conectado al RX del ESP32.

### Controlador B: ESP32 DevKit V1 (Interfaz Web)
- **Framework:** MicroPython
- **Responsabilidad:** Levantar el servidor web asíncrono, gestionar WiFi, proveer la interfaz de control y transmitir comandos UART.
- **Asignación de Pines:**
  - UART TX: GPIO 17 (Conectado a RX del Nano).
  - UART RX: GPIO 16 (Conectado a TX del Nano).
  - LED Status: GPIO 2.

---

## 2. Requerimientos de Software

### Tarea 1: Firmware Arduino (`arduino/grúa_arduino.ino`)
- **Control de Velocidades Máximas:** Definir constantes configurables al inicio del archivo para establecer los límites máximos de velocidad PWM (rango 0-255) de cada motor: `MAX_SPEED_CARRO`, `MAX_SPEED_ELEVACION` y `MAX_SPEED_GIRO`.
- **Conmutación de Modo Sincronizada:**
  - Iniciar por defecto en Modo Web (`manualMode = false`).
  - Escuchar comandos UART `MM` (Modo Manual) y `MW` (Modo Web) para actualizar la variable de estado.
  - Leer el pin digital D6 (Pulsador del Joystick 2) usando lógica anti-rebote (debounce). Al ser presionado, conmutar el modo de control.
  - Al cambiar de modo (por botón o por comando UART), transmitir inmediatamente por puerto serie `MOD:MANUAL` o `MOD:WEB`.
- **Control de Motores en Modo Manual:**
  - Leer entradas analógicas A0 (Carro), A1 (Elevación) y A2 (Giro).
  - Implementar una zona muerta (deadzone) de ±30 en torno a la lectura central (~512) para evitar micro-movimientos por ruido.
  - Mapear linealmente la desviación del joystick hacia el driver del motor correspondiente en el rango `[0, MAX_SPEED_*]` según la dirección.
- **Control de Motores en Modo Web:**
  - Ignorar las señales analógicas de los joysticks.
  - Mover los motores a sus respectivas velocidades máximas definidas (`MAX_SPEED_*`) al recibir los comandos seriales correspondientes:
    - `CL` / `CR`: Carro Izquierda / Derecha.
    - `EU` / `ED`: Elevación Arriba / Abajo.
    - `GL` / `GR`: Giro Izquierda / Derecha.
    - `S`: Detener todos los motores.
- **Estimación de Ángulo:**
  - Calcular el ángulo actual de giro de la pluma integrando en software el tiempo que permanece encendido el motor de Giro.
  - Asumir que a máxima velocidad (PWM 255) la pluma rota a 30 RPM (180° por segundo), reduciéndose proporcionalmente a menor valor de PWM.
  - Reportar periódicamente el ángulo al ESP32 enviando `ANG:<valor_entero>\n` por Serial.
- **Seguridad (Timeout):** En modo Web, si no se recibe ningún comando serial válido en 2000 ms, los motores se deben detener automáticamente.

### Tarea 2: Firmware ESP32 (`esp32/main.py`)
- **Transmisión y Lectura UART:**
  - Tarea asíncrona dedicada a escuchar la entrada serie del Arduino.
  - Al recibir `MOD:MANUAL` o `MOD:WEB`, actualizar el estado interno `control_mode`.
  - Al recibir `ANG:<valor>`, actualizar el valor del ángulo actual `current_angle`.
- **Servidor Web y Endpoints:**
  - `/`: Entrega la interfaz HTML/JS responsiva con tema oscuro.
  - `/telemetry`: Devuelve JSON con el estado de sincronización: `{"angle": current_angle, "mode": control_mode}` (donde `control_mode` es `"manual"` o `"web"`).
  - `/control?cmd=<cmd>`: Procesa comandos de control y los envía al Arduino. Soporta además `mode_manual` (envía `MM`) y `mode_web` (envía `MW`).

### Tarea 3: Interfaz Web
- Agregar un selector/switch toggle premium que permita conmutar entre control manual y control web.
- El switch debe actualizar su estado visual en base a las consultas de telemetría (para reflejar cambios hechos con el botón físico).
- Si el modo activo es Manual, los botones de movimiento en la web se deben deshabilitar y mostrar un indicador de "Control Manual por Joysticks Activo".

---

## 3. Consideraciones Técnicas
- **Baudrate:** 9600 bps.
- **Tierra Común:** El Arduino y el ESP32 deben compartir GND para garantizar niveles lógicos estables en UART.