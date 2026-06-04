# to_gcode

Servicio de conversión de archivos SVG a instrucciones G-code para máquinas de trazado (Plotters).

## 🚀 Propósito
Automatizar la generación de trayectorias para máquinas tipo "Writing Pen Machine", transformando diseños vectoriales en dibujos físicos con escalado automático e inversión de ejes.

## 🛠 Stack Tecnológico
- **Lenguaje**: Python 3.12+
- **Framework API**: FastAPI
- **Persistencia**: SQLite + SQLAlchemy 2.0 (Modern Mapped)
- **Configuración**: Pydantic Settings (.env)
- **Logging**: Estandarizado (FastAPI style)
- **Procesamiento Geométrico**: svgpathtools
- **Generación G-code**: pygcode

## 🏗 Estructura del Proyecto (Clean Architecture)
- src/domain: Entidades puras y **Domain Services** (Geometría).
- src/application: Casos de uso y **Boundaries** (Interfaces).
- src/adapters: 
  - controllers: Lógica agnóstica de entrega.
  - gateways: Adaptadores para librerías externas y persistencia.
- src/infrastructure: 
  - fastapi: Configuración de servidor, rutas y DI.
  - database: Implementación de persistencia y modelos SQL.
  - settings: Configuración global y logger.
  - svgpathtools / pygcode: Wrappers técnicos.

## 📋 Estado del Proyecto
- **MVP (Completado)**: Conversión SVG a G-code (M3/M5) con persistencia de configuración y API REST.
- **Fase Actual**: Pruebas Unitarias y de Integración.
