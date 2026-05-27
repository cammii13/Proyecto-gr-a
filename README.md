# Control de Grúa Torre - Sistema de Control Dual

Este proyecto implementa el control dual (Manual por Joysticks y Remoto mediante Interfaz Web) de una grúa torre de tres ejes. El sistema está compuesto por un ESP32 que funciona como Servidor Web y un Arduino Nano que interactúa directamente con los sensores y actuadores (motores DC).

## Arquitectura de Hardware

```
+------------------+       UART       +-------------------+
|      ESP32       | <--------------> |   Arduino Nano    |
|  (Servidor Web)  |                  | (Control Motores) |
| - Conexión WiFi  |                  | - 3 Motores DC    |
| - Interfaz Web   |                  | - Joysticks (x2)  |
| - Puente Serie   |                  | - Botón de Modo   |
+------------------+                  +-------------------+
         |                                      |
         | HTTP                                 | Potencia (12V)
         v                                      v
+------------------+                  +-------------------+
|   Cliente Web    |                  |  TB6612FNG (x2)   |
| (Navegador Web)  |                  | (Puentes H Motores|
+------------------+                  +-------------------+
```

- **ESP32:** Gestiona la red WiFi, levanta un servidor web asíncrono y se comunica de manera bidireccional por puerto serie (UART) con el Arduino.
- **Arduino Nano:** Ejecuta la lectura en tiempo real de los joysticks analógicos y del interruptor físico, realiza la estimación del ángulo de rotación de la pluma por software e implementa el control de velocidad/dirección para los tres motores DC.
- **Drivers de Motor (TB6612FNG):** Dos puentes H integrados. El primero controla el Carro (eje horizontal) y la Elevación (eje vertical). El segundo controla el Giro (eje de rotación) utilizando solo uno de sus canales.

## Características Principales

1. **Control Dual Sincronizado:** Permite conmutar entre control desde la Web y control Manual (Joysticks) usando tanto un interruptor en la interfaz web como el botón físico del Joystick 2 (pin D6 de Arduino). Ambos controles sincronizan su estado automáticamente en tiempo real.
2. **Velocidad Máxima Configurable:** El archivo de Arduino permite configurar la velocidad PWM máxima de forma independiente para cada uno de los motores (`MAX_SPEED_CARRO`, `MAX_SPEED_ELEVACION`, `MAX_SPEED_GIRO`).
3. **Estimación de Ángulo en Software:** Integra la velocidad y dirección de giro del motor DC de rotación de 30 RPM para simular en tiempo real el ángulo exacto de la pluma (180°/segundo a velocidad máxima) y enviarlo al ESP32 por telemetría.
4. **Seguridad Integrada (Timeout):** En modo web, los motores se detienen automáticamente si no se recibe un comando serial válido en 2 segundos para evitar desplazamientos descontrolados.

## Esquema Electrónico de Conexiones

Para ver los detalles del conexionado y pines utilizados, abre el archivo interactivo:
- **[Ver Esquema de Conexiones (Schema.html)](Schema.html)**

## Instrucciones de Instalación y Despliegue

### Requisitos
- ESP32 con MicroPython instalado.
- Arduino Nano con Arduino IDE.
- Fuente de alimentación externa (12V para motores y 5V lógica).

### Despliegue ESP32
1. Conéctalo al ordenador.
2. Configura las credenciales WiFi en `esp32/boot.py`.
3. Sube `esp32/boot.py` y `esp32/main.py`.
4. Reinicia el ESP32, se conectará a WiFi y te mostrará la IP en la consola serie. Accede a `http://<IP_ESP32>/` desde tu navegador.

### Despliegue Arduino
1. Abre `arduino/grúa_arduino.ino` en Arduino IDE.
2. Sube el firmware a tu Arduino Nano.
3. Conecta el cableado de acuerdo al diagrama interactivo `Schema.html`.

## Documentación Técnica Detallada

- [Requerimientos Técnicos](/docs/requirements.md)
- [Especificación del API](/docs/api_spec.md)
- [Características del Sistema](/docs/features.md)
