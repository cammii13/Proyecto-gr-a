## 1. Documentación y Esquema Electrónico

- [ ] 1.1 Mover `docs/README.md` a la raíz `README.md` y actualizar su contenido
- [ ] 1.2 Eliminar `docs/README.md` de la carpeta `docs`
- [ ] 1.3 Optimizar y actualizar `docs/requirements.md`, `docs/api_spec.md` y `docs/features.md`
- [ ] 1.4 Crear el archivo `Schema.html` en la raíz con el diagrama interactivo de conexiones

## 2. Firmware Arduino

- [ ] 2.1 Reemplazar control de motor a pasos por tercer motor DC (Giro) con TB6612FNG (2)
- [ ] 2.2 Agregar constantes de velocidad máxima configurables para los tres ejes
- [ ] 2.3 Implementar lecturas analógicas de joysticks y botón físico D6 con debounce para cambio de modo
- [ ] 2.4 Implementar estimación temporal del ángulo de giro (motor 30 RPM / 180° por segundo)
- [ ] 2.5 Actualizar protocolo UART bidireccional para soportar conmutación y sincronización de modo

## 3. Firmware ESP32 e Interfaz Web

- [ ] 3.1 Actualizar comandos de control UART y telemetría en `esp32/main.py`
- [ ] 3.2 Modificar `/telemetry` para incluir el estado de modo y manejar respuestas de sincronización
- [ ] 3.3 Diseñar e integrar switch de conmutación en la web y deshabilitar controles si está en manual
