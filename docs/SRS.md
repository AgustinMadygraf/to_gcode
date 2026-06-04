# Software Requirements Specification (SRS) - to_gcode

## 1. Alcance del MVP
- **Máquina**: Plotter Writing Pen.
- **Control**: Comandos M3 (bajar) / M5 (levantar).
- **Funcionalidad**: Conversión SVG -> G-code (M3/M5).
- **Configuración**: Persistencia en SQLite de parámetros de máquina (velocidad, área, comandos).

## 2. Arquitectura
- **Modelo**: Clean Architecture.
- **Capas**: Domain, Application (with Contracts), Adapters, Infrastructure.

## 3. Requerimientos Técnicos
- Persistencia mediante SQLAlchemy.
- API REST con FastAPI.
- Desacoplamiento de `svgpathtools` y `pygcode` mediante Gateways en la capa de adaptadores.
