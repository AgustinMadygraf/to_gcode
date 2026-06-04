# Guía del Proyecto - to_gcode

## Convenciones de Desarrollo
- **Arquitectura**: Clean Architecture estricta.
- **Flujo de Dependencias**: Las dependencias siempre apuntan hacia el interior (Domain <- Application <- Adapters <- Infrastructure).

## Estructura de Capas
1. **Domain**: Independiente de todo.
2. **Application**: Contiene los casos de uso y depende solo del dominio.
3. **Adapters**: Implementa las interfaces de aplicación para DB, APIs y librerías externas.
4. **Infrastructure**: Detalles técnicos y configuración de frameworks.
