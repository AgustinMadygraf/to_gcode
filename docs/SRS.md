# Software Requirements Specification (SRS) - to_gcode

## 1. Alcance del MVP
- Máquina: Plotter Writing Pen.
- Control: Comandos M3 bajar / M5 levantar configurables.
- Funcionalidad: Conversión SVG -> G-code con escalado proporcional automático.
- Persistencia: SQLite para parámetros de máquina.

## 2. Arquitectura Final
- Modelo: Clean Architecture.
- Capas: Domain (Entities/Services), Application (Use Cases/Boundaries), Adapters (Controllers/Gateways), Infrastructure.

## 3. Requerimientos Técnicos
- Persistencia: SQLAlchemy 2.0 con tipado moderno.
- API REST: FastAPI con eventos de ciclo de vida (Lifespan).
- Configuración: Variables de entorno (.env) vía Pydantic Settings.
- Logging: Sistema centralizado estilo FastAPI.
- Desacoplamiento: Uso de wrappers técnicos para svgpathtools y pygcode.
