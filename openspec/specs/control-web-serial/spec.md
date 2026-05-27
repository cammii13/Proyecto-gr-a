# control-web-serial Specification

## Purpose
TBD - created by archiving change control-serial-web-y-debug-inalambrico. Update Purpose after archive.
## Requirements
### Requirement: Conexión Web Serial USB
La interfaz de usuario en `index.html` MUST permitir establecer una conexión directa con el puerto serie USB del Arduino Nano a través de la Web Serial API al hacer click en el botón "Conectar USB".

#### Scenario: Conexión exitosa del puerto serie en navegador
- **WHEN** el usuario hace click en el botón "Conectar USB" y selecciona el puerto correspondiente
- **THEN** el navegador abre la comunicación serie a 9600 baudios, cambia el estado del botón a "Conectado" y arranca el lector asíncrono de telemetría.

### Requirement: Telemetría por JSON Serie
El Arduino Nano MUST enviar tramas de telemetría JSON formateadas como `{"angle": <int>, "mode": "web"|"manual"}` por el puerto serie USB principal. La interfaz web SHALL parsear y procesar estas tramas para actualizar el indicador de la pluma y la posición del interruptor de modo.

#### Scenario: Recepción de trama JSON de telemetría
- **WHEN** llega la trama `{"angle":150,"mode":"web"}\n` al puerto serie del navegador
- **THEN** el Javascript de la interfaz parsea la cadena y actualiza la aguja indicadora a 150 grados y activa el modo Web en la pantalla.

