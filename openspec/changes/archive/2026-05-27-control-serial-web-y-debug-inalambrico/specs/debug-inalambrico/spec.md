## ADDED Requirements

### Requirement: Almacenamiento de Trazas (Logs)
El firmware del ESP32 MUST leer de forma continua las trazas de texto del puerto UART secundario (pines 16/17) enviadas por el Arduino Nano y almacenar las últimas 50 líneas en un búfer circular en RAM.

#### Scenario: Adición de nueva línea de log al búfer
- **WHEN** llega la línea "Motor Carro moviéndose a la izquierda\n" por SoftwareSerial a la UART del ESP32
- **THEN** se agrega la traza al búfer circular, eliminando la línea más antigua si el tamaño excede de 50.

### Requirement: Servidor de Depuración y Terminal Retro
El ESP32 MUST alojar un servidor socket web en el puerto 80 que entregue una interfaz minimalista de terminal (estética retro de texto verde `#00ff00` sobre fondo negro) y que se auto-refresque automáticamente cada 2 segundos.

#### Scenario: Visualización remota de logs desde celular
- **WHEN** el programador abre la dirección IP del ESP32 en el navegador de su celular
- **THEN** el ESP32 retorna una página HTML con el listado de logs formateado como terminal, la cual incluye la directiva de refresco `<meta http-equiv="refresh" content="2">`.
