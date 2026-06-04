# Documentación de la API - to_gcode

## Visión General
Esta API permite configurar parámetros de máquina plotter y convertir archivos SVG a G-code siguiendo Clean Architecture.

## Endpoints

### 1. Configuración
- **POST /config**: Establece o actualiza la configuración de la máquina.
  - Payload: ConfigSchema (name, width, height, etc.)
  - Respuesta: 201 Created
- **GET /config**: Recupera la configuración actual.
  - Respuesta: 200 OK + ConfigSchema

### 2. Conversión
- **POST /convert**: Convierte un archivo SVG subido.
  - Payload: Multipart file (file)
  - Respuesta: 200 OK + {"gcode": "..."}
  - Error: 400 Bad Request (SVG inválido o configuración no encontrada)

## Acceso Interactivo
- **Swagger UI**: /docs
- **ReDoc**: /redoc
