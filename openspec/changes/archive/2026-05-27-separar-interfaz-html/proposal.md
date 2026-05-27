## Why

Actualmente la interfaz de usuario de la grúa torre (HTML/CSS/JS) se encuentra incrustada directamente como una cadena multilinea dentro de `esp32/main.py`. Esto dificulta el desarrollo, el mantenimiento y la legibilidad del código tanto de Python como del frontend. Separar la interfaz en un archivo `index.html` independiente mejora la organización del proyecto y permite editar el diseño con herramientas HTML estándar.

## What Changes

- Creación de un archivo `esp32/index.html` que contiene todo el código HTML/CSS/JS de la interfaz.
- Modificación de `esp32/main.py` para eliminar la cadena HTML de su código.
- Actualización de la función de enrutamiento web en `esp32/main.py` para abrir y leer de forma no bloqueante el archivo `index.html` antes de enviarlo al cliente.

## Capabilities

### New Capabilities
- `separar-interfaz`: Permite servir la interfaz web de control desde un archivo HTML independiente en el sistema de archivos local del ESP32.

### Modified Capabilities

## Impact

- **Firmware ESP32 (`esp32/main.py`)**: Remoción de la variable HTML e implementación de la lectura dinámica del archivo en el sistema de archivos local de MicroPython.
- **Frontend (`esp32/index.html`)**: Nuevo archivo HTML.
