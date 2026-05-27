# control-dual-motor-dc Specification

## Purpose
TBD - created by archiving change actualizar-motores-y-control. Update Purpose after archive.
## Requirements
### Requirement: Control Dual Manual/Web Sincronizado
El sistema MUST permitir la conmutación entre el modo de control Manual (vía Joysticks) y el modo de control Web. La conmutación SHALL realizarse tanto al presionar el botón físico del Joystick 2 (pin D6) como al interactuar con el interruptor en la interfaz web. El estado actual del modo MUST estar sincronizado en ambos controladores (Arduino y ESP32) y reflejado en tiempo real en la interfaz web.

#### Scenario: Conmutación desde botón físico de Joystick 2
- **WHEN** el usuario presiona el botón físico en el pin D6 de Arduino Nano
- **THEN** Arduino Nano cambia el modo actual de control, transmite por UART el nuevo estado y el ESP32 actualiza su estado local y la interfaz web para reflejar el cambio.

#### Scenario: Conmutación desde interruptor de la Web
- **WHEN** el usuario hace click en el interruptor de modo de la interfaz web
- **THEN** el ESP32 envía el comando de cambio de modo al Arduino Nano vía UART, el Arduino cambia el modo y confirma el nuevo estado por serial, bloqueando o desbloqueando los botones de la interfaz web según corresponda.

### Requirement: Ajuste de Velocidad de Motores DC
El firmware de Arduino MUST permitir configurar límites de velocidad máxima independientes para cada uno de los tres motores DC: Carro, Elevación y Giro, usando constantes configurables en el código. En modo manual, las lecturas de los joysticks analógicos SHALL ser mapeadas proporcionalmente a las velocidades de los motores respetando dichos límites máximos.

#### Scenario: Regulación de velocidad manual con joystick
- **WHEN** el usuario mueve el eje X del Joystick 1
- **THEN** el Arduino Nano lee el pin A0, calcula la velocidad proporcional al desplazamiento fuera de la zona muerta, y aplica el valor de PWM al driver de motor de Carro sin exceder la constante de velocidad máxima configurada en el archivo.

### Requirement: Estimación de Ángulo de Giro de la Pluma
Al no contar con un motor a pasos o sensor absoluto, el Arduino Nano MUST estimar el ángulo de rotación de la pluma en software integrando en el tiempo el movimiento del motor de giro de 30 RPM (que a máxima velocidad gira a 180° por segundo). Este ángulo estimado SHALL ser reportado periódicamente al ESP32 a través de comandos `ANG:<valor>\n`.

#### Scenario: Reportar ángulo estimado de rotación
- **WHEN** el motor de Giro se activa hacia la derecha durante 1 segundo a máxima velocidad
- **THEN** el ángulo estimado aumenta en 180 grados y se reporta el nuevo ángulo al ESP32 vía UART.

