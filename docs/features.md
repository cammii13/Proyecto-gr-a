# Características del Proyecto

Este documento describe las funcionalidades principales del sistema de control de la grúa torre.

## Menú de Inicio interactivo (`boot.py`)

Al arrancar el ESP32, `boot.py` muestra un menú interactivo en la consola serial que permite elegir el modo de operación:

```
========================================
      SISTEMA DE CONTROL - GRÚA TORRE
========================================
1. Iniciar sistema normalmente (Modo Ejecución)
2. Detener en modo programación (Liberar REPL)
Selecciona una opción (Avanza a opción 1 en 5s)...
```

- Opción 1 (o timeout de 5s): el ESP32 se conecta automáticamente a la red WiFi y arranca el servidor web contenido en `main.py`.
- Opción 2: detiene la ejecución automática y libera la consola REPL para programación y depuración.
- Este menú facilita el desarrollo in situ y el arranque seguro en entornos de producción.

## Frenado automático en Arduino (timeout de 2s)

El firmware de Arduino implementa un mecanismo de seguridad que detiene todos los motores si no se reciben comandos por UART durante 2 segundos:

- Variable `TIMEOUT = 2000` (ms).
- `lastCommandTime` se actualiza al recibir cualquier comando válido por serial.
- En el bucle principal (`loop()`), si `millis() - lastCommandTime > TIMEOUT` se llama a `stopAllMotors()`.

Este comportamiento previene desplazamientos continuos por pérdida de comunicación y mejora la seguridad operativa.

## Interfaz web asíncrona (modo oscuro)

La interfaz web servida por el ESP32 (`main.py`) es asíncrona y ofrece control remoto sin recargar la página:

- Servidor HTTP asíncrono usando `uasyncio`.
- Diseño responsive con tema oscuro (fondo `#121212`) para operación en entornos con baja luminosidad.
- Controles para los tres ejes: carro (izq/der), elevación (arriba/abajo) y giro (izq/der), más botón de emergencia `PARAR`.
- Comunicación con el ESP32 desde el front-end mediante `fetch()` hacia el endpoint `/control?cmd=<comando>` para enviar comandos UART al Arduino.
- Feedback en tiempo real en un indicador de estado en la página.

Estas características proporcionan una experiencia de control remota fluida y clara para operadores.
