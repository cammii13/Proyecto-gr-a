# separar-interfaz Specification

## Purpose
TBD - created by archiving change separar-interfaz-html. Update Purpose after archive.
## Requirements
### Requirement: Servir Interfaz desde Archivo
El servidor web asíncrono del ESP32 MUST leer el archivo `index.html` del sistema de archivos local cuando se reciba una petición GET en la ruta raíz `/`.

#### Scenario: Lectura y entrega exitosa de la interfaz
- **WHEN** el usuario realiza una petición GET a `http://<IP_ESP32>/`
- **THEN** el sistema lee el archivo `index.html` del sistema de archivos local y devuelve su contenido completo como tipo de contenido `text/html` con código de estado HTTP 200.

### Requirement: Robustez ante Errores de Lectura
Si por algún motivo el archivo `index.html` no se encuentra en el sistema de archivos del ESP32 o no puede ser leído, el servidor web MUST manejar la excepción elegantemente sin caerse, y retornar un mensaje de error legible para el usuario.

#### Scenario: Archivo index.html faltante en flash
- **WHEN** el usuario realiza una petición GET a `/` pero el archivo `index.html` no existe en la flash del ESP32
- **THEN** el servidor web captura el error, responde con código de estado HTTP 500 y muestra el texto "Error 500: Archivo index.html no encontrado en la memoria del dispositivo".

