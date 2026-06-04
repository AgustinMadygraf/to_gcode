# Frontend - Arquitectura y Convenciones

## Arquitectura Modular (ES Modules)
El frontend ha sido refactorizado siguiendo principios de Arquitectura Limpia y DDD. Se utiliza JavaScript puro con soporte de módulos ES (type="module" en el script principal).

## Estructura de Carpetas
- /frontend/js/domain/: Entidades de negocio (ej. MachineConfig). Reglas de validación pura.
- /frontend/js/infrastructure/: Detalles técnicos y comunicación (ej. ApiGateway). Abstracción de fetch.
- /frontend/js/app.js: Controlador de UI. Orquestador de eventos, DOM y delegación de lógica a capas inferiores.

## Estándares de Diseño
- CSS: Uso exclusivo de Bootstrap 5. Se han eliminado estilos personalizados en favor de clases de utilidad (shadow-sm, bg-light, etc.).
- Manejo de Errores: Centralizado en app.js. Las capas domain e infrastructure lanzan errores puros, app.js los captura para loguear (console.error, console.warn) y comunicar al usuario (alert).

## Funcionalidades
- Configuración de Máquina: Gestión de parámetros mediante la entidad MachineConfig.
- Conversión de SVG:
    - Archivo local (Multipart).
    - URL externa (vía backend para evitar CORS).
    - Modo Test: Opcional, limita la salida a 100 líneas de GCode.
