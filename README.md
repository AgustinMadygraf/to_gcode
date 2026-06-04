# to_gcode

Servicio de conversión de archivos SVG a instrucciones G-code para máquinas de trazado (Plotters).

## 🚀 Propósito
Automatizar la generación de trayectorias para máquinas tipo "Writing Pen Machine", transformando diseños vectoriales en dibujos físicos.

## 🛠 Stack Tecnológico
- **Lenguaje**: Python 3.12+
- **Framework API**: FastAPI
- **Persistencia**: SQLite + SQLAlchemy
- **Procesamiento Geométrico**: svgpathtools
- **Generación G-code**: pygcode
- **Arquitectura**: Clean Architecture (Arquitectura Limpia)

## 🏗 Estructura del Proyecto
- `src/domain`: Entidades y reglas de negocio puras.
- `src/application`: Casos de uso y contratos (interfaces).
- `src/adapters`: Controladores, repositorios y gateways.
- `src/infrastructure`: Frameworks (FastAPI) y Drivers (SQLAlchemy).

## 📋 Estado del Proyecto
- **MVP**: Conversión pura (M3/M5) con persistencia de configuración.
