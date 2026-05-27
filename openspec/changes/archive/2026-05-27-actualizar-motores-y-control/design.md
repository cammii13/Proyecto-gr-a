## Context

El sistema de control de la grúa torre utiliza actualmente un motor a pasos Nema 17 para la rotación (Giro) y dos motores DC N20 para carro y elevación. El Giro es controlado mediante señales de paso/dirección a un driver DRV8825. Se desea simplificar el sistema físico utilizando un motoreductor DC de 30 RPM para el eje de Giro, requiriendo un segundo driver TB6612FNG y liberando los pines del driver de pasos.
Además, se requiere poder operar la grúa de forma manual mediante joysticks físicos cuando el usuario lo desee, sincronizando el estado con la interfaz web.

## Goals / Non-Goals

**Goals:**
- Conectar y configurar el tercer motor DC para Giro utilizando un segundo puente H TB6612FNG (canal A).
- Permitir la configuración de velocidad máxima (0-255 PWM) para los tres motores.
- Implementar el control manual analógico con joysticks y la conmutación de modo (Manual vs Web) de forma sincronizada y fluida.
- Estimar el ángulo de giro mediante integración temporal en el firmware.
- Actualizar el protocolo serie para comunicar el cambio de modo.

**Non-Goals:**
- Implementar un encoder físico de retroalimentación cerrada para el giro (se utilizará estimación por software).
- Agregar otros controles a la interfaz web aparte del switch de modo y de los controles existentes.

## Decisions

### 1. Estimación de Ángulo en Software para Giro DC
- **Alternativa A:** Utilizar un encoder de cuadratura físico. *Descartado* por no requerir cables ni componentes extras, además de mantener el cableado original intacto.
- **Alternativa B:** Simular la posición en base al tiempo de encendido y la velocidad enviada al motor de giro. *Seleccionada*. La velocidad máxima del motor es de 30 RPM (0.5 rev/s = 180°/s). Por lo tanto, el ángulo se incrementará o decrementará proporcionalmente a la velocidad del PWM aplicada por unidad de tiempo (`delta_angle = (PWM / 255.0) * 180.0 * dt`).

### 2. Protocolo de Conmutación de Modo Sincronizado
- **Decisión:** Usar dos nuevos comandos UART: `MM\n` (modo manual) y `MW\n` (modo web).
  - Al cambiar de modo desde la Web: El ESP32 envía `MM` o `MW` a Arduino. Arduino actualiza su variable de estado y responde con `MOD:MANUAL` o `MOD:WEB` para confirmar.
  - Al cambiar de modo físicamente (botón D6): Arduino cambia de estado, y transmite inmediatamente por Serial `MOD:MANUAL` o `MOD:WEB`. El ESP32 lee este mensaje y actualiza su estado local.
  - El endpoint de telemetría `/telemetry` devuelve `{"angle": current_angle, "mode": control_mode}` para sincronizar la interfaz web mediante sondeo (polling).

## Risks / Trade-offs

- **Desviación del ángulo estimado:** Al no tener encoder, la posición real puede desalinearse con respecto a la posición estimada con el tiempo debido a inercia o fricción.
  - *Mitigación:* Se implementará un mecanismo simple de estimación libre de derivas complejas, asumiendo que los movimientos son cortos. El usuario puede reposicionar la pluma manualmente si es necesario.
- **Ruido en lecturas analógicas del Joystick:** Las variaciones en la señal analógica del joystick podrían causar micro-movimientos indeseados en los motores en modo manual.
  - *Mitigación:* Se implementará una "zona muerta" (deadzone) de ±30 unidades alrededor de la lectura central (normalmente 512).
