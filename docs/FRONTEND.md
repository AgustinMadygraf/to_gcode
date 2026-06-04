# Frontend de to_gcode

El frontend es una aplicación ligera utilizando **HTML5 + Bootstrap 5 (CSS)** y **JavaScript nativo (Vanilla JS)**.

## Estructura
- frontend/index.html: UI principal con Bootstrap.
- frontend/js/app.js: Lógica de interacción y llamadas a la API.
- frontend/css/style.css: Estilos personalizados.

## Interacción con la API
Se utiliza la API Fetch (fetch()) para comunicarse con el backend:
- POST /config: Enviar configuración.
- GET /config: Obtener configuración actual.
- POST /convert: Subir SVG y descargar G-code.
