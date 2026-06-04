# API Documentation

## Endpoints

### 1. Configuración
- GET /config: Obtiene la configuración actual de la máquina.
- POST /config: Guarda la configuración de la máquina.

### 2. Conversión
- POST /convert: Convierte un archivo SVG local a GCode.
    - Multipart form: file (SVG), test_mode (boolean, optional).
- POST /convert/url: Convierte un SVG desde una URL remota a GCode.
    - JSON: {"url": "...", "test_mode": boolean}.

## Notas
- El parámetro test_mode=true trunca la salida a las primeras 100 líneas.
