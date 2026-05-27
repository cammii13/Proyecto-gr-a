## Context

El ESP32 corre MicroPython y sirve una interfaz web de control. El código HTML estaba embebido en `main.py`. Al separar la interfaz a `index.html`, debemos leer el archivo del sistema de archivos local (flash) de forma robusta e integrada en el flujo asíncrono de `uasyncio`.

## Goals / Non-Goals

**Goals:**
- Servir la interfaz leyendo dinámicamente `index.html`.
- Ofrecer un mensaje de contingencia en caso de que ocurra algún error al leer el archivo.

**Non-Goals:**
- Cambiar la lógica interna del protocolo UART o del control de motores.
- Añadir compresión o optimización de bytes en la transmisión del HTML (se enviará en texto plano).

## Decisions

### 1. Lectura de Archivo local
- **Decisión:** Utilizar la sintaxis nativa de Python `with open('index.html', 'r', encoding='utf-8') as f:` para leer todo el archivo HTML en memoria. Al ser un archivo de aproximadamente 7-8 KB, cabe holgadamente en la RAM disponible de la pila MicroPython del ESP32.
- **Alternativa Considerada:** Cargar el archivo línea por línea para streaming. *Descartada* porque incrementa la complejidad del enrutador y la latencia de respuesta HTTP sin justificación de memoria real para este tamaño de archivo.

## Risks / Trade-offs

- **Falta del archivo index.html en Flash:** Si el usuario olvida subir el archivo `index.html` pero sube `main.py`, el servidor lanzará una excepción al consultar `/`.
  - *Mitigación:* Capturar cualquier `OSError` e interceptarlo para devolver una respuesta HTML de contingencia "Error 500: index.html no encontrado".
