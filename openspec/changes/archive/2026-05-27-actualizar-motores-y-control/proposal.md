## Why

El proyecto requiere migrar de un motor a pasos para el eje de giro a un motoreductor DC de 30 RPM, lo cual simplifica la mecánica y unifica el tipo de motores de los tres ejes a motores DC. Asimismo, se necesita control local manual mediante joysticks físicos con un selector de modo (manual/web) que pueda alternarse de forma síncrona tanto físicamente (botón del joystick) como digitalmente (interfaz web).

## What Changes

- Reemplazo del motor a pasos por un motoreductor DC para el giro (Giro) controlado mediante un segundo puente H TB6612FNG.
- Configuración de velocidades máximas independientes para los tres motores en el firmware del Arduino.
- Lectura de señales analógicas de dos joysticks para controlar los tres ejes en modo manual.
- Incorporación de un botón físico (Joystick 2 SW conectado a D6) y un switch en la interfaz web para conmutar el modo de control (Manual/Web).
- Estimación en software del ángulo de orientación de la pluma (giro).
- Actualización de la comunicación serial bidireccional entre ESP32 y Arduino Nano para reportar y cambiar el modo de control.
- Creación de un esquema electrónico interactivo en `Schema.html` y actualización de la documentación del proyecto, moviendo el README a la raíz.

## Capabilities

### New Capabilities
- `control-dual-motor-dc`: Permite controlar la grúa torre mediante interfaz web o joysticks físicos de manera excluyente, conmutando el estado síncronamente y regulando la velocidad de tres motores DC según límites establecidos.

### Modified Capabilities

## Impact

- **Firmware Arduino (`arduino/grúa_arduino.ino`)**: Reemplazo de `AccelStepper` por lógica de motor DC, lectura analógica de joysticks, lógica de botón de modo en pin D6, y protocolo UART bidireccional.
- **Firmware ESP32 (`esp32/main.py`)**: Actualización de la interfaz HTML/JS para incluir el interruptor de modo, actualización del endpoint de telemetría para incluir el modo activo, y retransmisión UART del modo.
- **Documentación**: Movimiento de `README.md` a la raíz y actualización de la documentación técnica.
