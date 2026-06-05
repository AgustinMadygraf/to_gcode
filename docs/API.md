# API Documentation

## Endpoints

### 1. Configuración
- GET /config: Obtiene la configuración actual de la máquina.
- POST /config: Guarda la configuración de la máquina.

### 2. Conversión
- POST /convert: Convierte un archivo SVG local a GCode.
    - Multipart form: file (SVG).
- POST /convert/image: Convierte un archivo de imagen local a GCode.
    - Multipart form: file (Image).
- POST /convert/url: Convierte un SVG desde una URL remota a GCode.
    - JSON: {"url": "..."}.

## Notas
- El comportamiento de truncamiento de G-code está ahora configurado exclusivamente a través de variables de entorno del servidor (GCODE_TRUNCATE_LIMIT) y no es controlado por la API.
