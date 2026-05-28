## Why

El ESP32 experimenta inestabilidad de memoria al servir una interfaz gráfica pesada al mismo tiempo que procesa ráfagas de comandos HTTP en tiempo real. Para resolver esto, migraremos el control principal a una conexión directa USB desde el navegador usando Web Serial API (reduciendo la carga en el ESP32), y reorientaremos el ESP32 para que actúe únicamente como monitor de logs de depuración inalámbrico.

## What Changes

- **Control Principal por Web Serial (USB):** La interfaz web se carga localmente y se conecta directamente al Arduino Nano por puerto serie a través de la Web Serial API.
- **Canal de Logs Secundario (SoftwareSerial):** Configuración de un puerto serie por software en Arduino (pines D10/D13) conectado al ESP32 para transmitir trazas de logs de depuración.
- **Monitor Inalámbrico de Depuración en ESP32:** El ESP32 lee de su puerto serie secundario y aloja las últimas 50 líneas de logs en RAM, sirviendo una interfaz terminal retro HTML auto-refrescable cada 2 segundos.
- **Reorganización de Archivos:** Estructura de carpetas `/arduino/`, `/esp32/` y `/web_server/`. Eliminación de archivos obsoletos de la raíz.

## Capabilities

### New Capabilities
- `control-web-serial`: Control local por cable USB desde la interfaz HTML mediante Web Serial API.
- `debug-inalambrico`: Consola de depuración en tiempo real expuesta por el ESP32 mediante servidor socket web con logs del Arduino Nano.

### Modified Capabilities

## Impact

- **Firmware Arduino (`arduino/grúa_arduino.ino`)**: Integración de SoftwareSerial, redirección de logs, y telemetría por JSON serializado en el canal principal USB.
- **Firmware ESP32 (`esp32/main.py`)**: Remoción de interfaz de control, almacenamiento en búfer de logs seriales y entrega de terminal HTML retro.
- **Interfaz Web (`web_server/index.html` y `schema.html`)**: Incorporación de botones de navegación cruzada, lógica Web Serial API en index.html, y actualización del esquema con SoftwareSerial en schema.html.
