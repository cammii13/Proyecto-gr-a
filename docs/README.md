# Proyecto Grúa Torre

## Diagrama de Arquitectura

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

- ESP32: servidor web y puente UART.
- Arduino Nano: control de motores y lectura de sensores.
- Comunicación: HTTP para la interfaz web, UART para los comandos hacia Arduino.

## Instrucciones de Instalación y Despliegue

### Requisitos
- ESP32 con MicroPython instalado.
- Arduino Nano con Arduino IDE.
- Conexión WiFi disponible.
- Librerías: `AccelStepper` para Arduino y `uasyncio`/`network` en MicroPython.

### Despliegue ESP32
1. Conecta el ESP32 al PC por USB.
2. Sube `boot.py` y `main.py` desde Thonny u otro cliente MicroPython.
3. Configura las credenciales WiFi en `boot.py`.
4. Reinicia el ESP32 y espera el menú de inicio.
5. Selecciona iniciar normalmente (o espera el timeout) para arrancar el servidor web.
6. Accede a `http://<IP_ESP32>/` desde un navegador.

### Despliegue Arduino
1. Abre `arduino/grúa_arduino.ino` en Arduino IDE.
2. Instala la librería `AccelStepper`.
3. Verifica y sube el firmware al Arduino Nano.
4. Conecta ESP32 TX a Arduino RX y comparte masa común.

### Conexión y Arranque
- UART: ESP32 TX (GPIO 17) → Arduino RX (D0).
- Fuente de alimentación para ESP32 y Arduino.
- Inicia el sistema y verifica la conexión desde el navegador.

## Documentación Detallada

- [Especificación de API](/docs/api_spec.md)
- [Características y flujo del sistema](/docs/features.md)

---

> Bienvenido al proyecto de control de grúa torre. Usa esta guía para poner en marcha el sistema y consulta la documentación detallada en `docs/`.
