# to_gcode

Servicio de conversión de archivos SVG a instrucciones G-code para máquinas de trazado (Plotters).

## 🚀 Propósito
Automatizar la generación de trayectorias para máquinas tipo "Writing Pen Machine", transformando diseños vectoriales en dibujos físicos con escalado automático e inversión de ejes.

## 🛠 Stack Tecnológico
- **Backend**: Python 3.12+, FastAPI, SQLAlchemy 2.0, Pydantic Settings, Logging.
- **Frontend**: HTML5, Bootstrap 5, Vanilla JS (sin dependencias de build).

## 🏗 Arquitectura (Clean Architecture)
- **Domain**: Entidades y **Domain Services** (Geometría).
- **Application**: Casos de uso y **Boundaries** (Interfaces).
- **Adapters**: Controllers (Plain Python) y Gateways (Persistencia, Parsers).
- **Infrastructure**: FastAPI, SQLAlchemy, Logging, Wrappers técnicos.

## 📋 Estado del Proyecto
- **MVP (Backend Completado)**: Conversión SVG a G-code (M3/M5) con persistencia y API REST validada con tests unitarios y de integración.
- **Fase Actual**: Implementación de Frontend.

## 🔗 Documentación Adicional
- [Frontend Strategy](docs/FRONTEND.md)
- [SRS](docs/SRS.md)
- [Instrucciones Agente](AGENT.md)
