## 1. Reorganización y Limpieza de Archivos

- [ ] 1.1 Crear directorios `/arduino/`, `/esp32/` y `/web_server/`
- [ ] 1.2 Mover `grúa_arduino.ino` a `/arduino/`
- [ ] 1.3 Mover `boot.py` y `main.py` a `/esp32/`
- [ ] 1.4 Mover `esp32/index.html` y `Schema.html` a `/web_server/` renombrándolos en minúsculas (`index.html`, `schema.html`)
- [ ] 1.5 Eliminar archivos obsoletos o duplicados del directorio raíz del proyecto

## 2. Firmware Arduino

- [ ] 2.1 Importar `SoftwareSerial` y definir el puerto `debugSerial` en pines D10 (RX) y D13 (TX)
- [ ] 2.2 Configurar `Serial` para USB principal y `debugSerial` para ESP32 a 9600 bps
- [ ] 2.3 Redirigir trazas de log de estado a `debugSerial.println()`
- [ ] 2.4 Formatear y enviar la telemetría en JSON plano a través del puerto serie principal USB (`Serial`)

## 3. Firmware ESP32

- [ ] 3.1 Remover endpoints de control e interfaz anteriores de `esp32/main.py`
- [ ] 3.2 Programar la lectura UART(2) de trazas de log y guardarlas en una lista circular en RAM (máx. 50 líneas)
- [ ] 3.3 Levantar mini servidor socket web en puerto 80 que muestre los logs en formato de terminal retro con auto-refresco

## 4. Interfaz Web (index.html y schema.html)

- [ ] 4.1 Incorporar en `index.html` y `schema.html` enlaces de navegación simétricos en el encabezado
- [ ] 4.2 Diseñar y programar el botón "Conectar USB" con la lógica de Web Serial API en JavaScript
- [ ] 4.3 Programar el envío de comandos serie por USB al hacer clic en botones o presionar teclas
- [ ] 4.4 Actualizar en `schema.html` el diagrama SVG y la tabla para reflejar la conexión SoftwareSerial (D10/D13)
