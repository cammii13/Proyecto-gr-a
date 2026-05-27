# Características del Proyecto (v3)

Este documento detalla las funcionalidades principales implementadas en el sistema de control de la grúa torre.

## 1. Menú de Inicio Interactivo en ESP32 (`boot.py`)
Al arrancar el ESP32, se presenta un menú interactivo a través de la consola serial con un retardo de 5 segundos:
- **Opción 1 (por defecto):** Inicia el firmware normalmente, conectando a WiFi y levantando el servidor HTTP asíncrono.
- **Opción 2:** Interrumpe el arranque automático y libera la consola de comandos REPL, permitiendo la depuración del código en MicroPython.

## 2. Control de Velocidad Configurable
El firmware del Arduino Nano define constantes globales e independientes al inicio para configurar los límites de velocidad de los tres motores DC:
- `MAX_SPEED_CARRO`
- `MAX_SPEED_ELEVACION`
- `MAX_SPEED_GIRO`
Estas constantes toman valores de `0` a `255` (PWM) y limitan el movimiento tanto en el control por web como en el control analógico manual.

## 3. Conmutación de Modo Dual Sincronizada
El sistema cuenta con un selector de modo (Manual / Web) que sincroniza bidireccionalmente el estado entre Arduino y ESP32:
- **Cambio Físico:** Al presionar el botón del Joystick 2 (pin D6 de Arduino con filtrado de rebotes por software), el modo de control alterna. Arduino notifica al ESP32 vía serie (`MOD:MANUAL` o `MOD:WEB`).
- **Cambio Digital:** Al hacer click en el interruptor de la web, se envía una solicitud al ESP32 que a su vez escribe `MM` o `MW` por serie a Arduino. Arduino cambia su estado local y confirma la operación regresando `MOD:MANUAL` o `MOD:WEB`.
- La interfaz web se adapta en tiempo real: si el modo es Manual, se bloquea el control web para evitar conflictos.

## 4. Control Manual por Joysticks con Zona Muerta
En el modo manual, el Arduino lee directamente los potenciómetros de los joysticks (ejes A0, A1, A2). Se implementa una zona muerta de ±30 en torno al centro (lectura 512) para filtrar el ruido eléctrico analógico de los mandos, impidiendo vibraciones o movimientos involuntarios del carro, elevación o giro.

## 5. Estimación de Orientación por Software (Giro DC)
Debido a la migración del motor paso a paso por un motoreductor DC de 30 RPM, la medición de orientación se calcula mediante estimación temporal en el Arduino Nano:
- Se asume que a velocidad máxima (PWM 255) el motor gira a 30 revoluciones por minuto (lo que equivale a 180° por segundo).
- El firmware integra en cada iteración del bucle `loop()` el desplazamiento en base a la velocidad actual y el sentido de giro.
- El ángulo estimado se normaliza en el rango `0` a `359` grados y es enviado automáticamente por puerto serie al ESP32 cuando este cambia.

## 6. Seguridad (Frenado por Timeout)
En **Modo Web**, el Arduino detiene de inmediato todos los motores si transcurren más de 2000 ms sin recibir comandos serie válidos. Esto previene movimientos continuos en caso de desconexión del cliente o caída del servidor web en el ESP32. En **Modo Manual**, el timeout está desactivado para dar control absoluto al operador local.
