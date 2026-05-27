## Context

El ESP32 sufre problemas de rendimiento al manejar control de tiempo real y servir la interfaz gráfica de forma concurrente. La Web Serial API nos permite transferir la responsabilidad de la conexión de control al navegador del cliente vía USB. El ESP32 pasará a operar en un puerto secundario de baja velocidad por software (`SoftwareSerial`) en Arduino para monitoreo y depuración remota libre de cables.

## Goals / Non-Goals

**Goals:**
- Configurar un canal de control por Web Serial API a 9600 bps sobre el puerto serie nativo de Arduino.
- Enviar telemetría formateada en JSON plano por el puerto USB.
- Configurar `SoftwareSerial` en Arduino (D10 RX, D13 TX) para enviar trazas de texto (logs).
- Implementar en el ESP32 la lectura del puerto serie secundario y servir la terminal retro de logs en el puerto 80.
- Estructurar el proyecto en `/arduino/`, `/esp32/` y `/web_server/`.

**Non-Goals:**
- Cambiar la lógica del controlador de motores ni el algoritmo de estimación de ángulo.
- Habilitar el control de la grúa desde el ESP32 (el control ahora es estrictamente por USB Web Serial).

## Decisions

### 1. Puerto Serie Secundario en Arduino
- **Decisión:** Utilizar los pines D10 (RX) y D13 (TX) con la librería estándar `SoftwareSerial` para la comunicación serie hacia el ESP32.
  - *Razones:* Estos pines se encuentran libres en el diagrama original tras retirar el motor a pasos, evitando conflictos en los puertos del controlador de motores y el hardware serie compartido con el programador USB de Arduino (D0/D1).

### 2. Formato de Logs Inalámbricos
- **Decisión:** Enviar logs en texto plano ASCII legible por humanos (ej. `[INFO] Carro Izquierda`). El ESP32 los acumulará en una lista FIFO (First-In, First-Out) de tamaño 50, simplificando el procesamiento de memoria en MicroPython.

### 3. Conexión de Control por Web Serial API
- **Decisión:** Integrar en `index.html` los métodos `navigator.serial.requestPort()` y `port.open({ baudRate: 9600 })` de Javascript. Cuando el puerto esté activo, un lector de flujos asíncrono recibirá las tramas JSON para actualizar la UI, y las llamadas a los botones escribirán directamente al escritor del flujo del puerto serie.

## Risks / Trade-offs

- **Compatibilidad del Navegador:** Web Serial API está soportado principalmente por navegadores basados en Chromium (Chrome, Edge, Opera) y no en Firefox o Safari.
  - *Mitigación:* Se mantendrá el fallback de fetch en el JavaScript de la web e indicación visual clara si la Web Serial API no está soportada por el navegador del operador.
