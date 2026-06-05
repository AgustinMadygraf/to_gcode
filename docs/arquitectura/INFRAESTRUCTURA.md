# Capa de Infraestructura - to_gcode

Esta capa contiene la implementación técnica de los detalles que el sistema necesita para funcionar. Sigue la regla de oro de Clean Architecture: **los detalles de infraestructura son intercambiables y no deben contaminar el Dominio ni la Aplicación**.

## Principios de Diseño
1. **Encapsulación Técnica:** Librerías externas (SQLAlchemy, FastAPI, PyGCode, scikit-image) están aisladas detrás de interfaces definidas en la capa de Aplicación.
2. **Implementación de Interfaces:** Todos los adaptadores de infraestructura implementan interfaces (DIP) definidas como boundaries en Aplicación.
3. **Configuración Centralizada:** El manejo de entorno, logger y parámetros globales está centralizado en `settings/`.

## Componentes Principales

### 1. Persistencia (src/infrastructure/database/)
- **SQLAlchemy:** Se utiliza como ORM para la persistencia.
- **Persistence Provider:** Implementa el contrato `ConfigPersistenceProvider` para desacoplar el motor de base de datos del repositorio de aplicación.
- **Migraciones/Modelos:** Define la estructura física de los datos (`MachineConfigModel`).

### 2. Integración Web (src/infrastructure/fastapi/)
- **FastAPI:** Framework web para exponer la API.
- **Rutas:** Mapean peticiones HTTP a los controladores de la capa de Adaptadores.
- **Inyección de Dependencias:** Gestión centralizada de la instanciación de servicios y controladores en `dependencies.py`.

### 3. Wrappers de Librerías (src/infrastructure/.../)
Encapsulan librerías de terceros complejas para que no filtren sus tipos de datos (como números complejos de `svgpathtools` o arrays de `numpy`) hacia las capas internas.
- **PyGCodeWrapper:** Traducción a sintaxis de código G.
- **SvgPathToolsWrapper:** Traducción de SVG a objetos geométricos del Dominio.
- **ScikitImageWrapper:** Procesamiento de imágenes (esqueletización).

## Gestión de Configuración y Logs
- **Settings:** Uso de `pydantic-settings` para carga segura de variables de entorno (.env).
- **Logger:** Configuración centralizada para asegurar una trazabilidad uniforme en todas las capas, vital para la depuración en producción.

## Auditoría Final
- **Aislamiento:** Verificado. No hay lógica de negocio en esta capa.
- **Flexibilidad:** Verificada. Cambiar una librería de infraestructura (ej. de SQLAlchemy a un ORM diferente o de FastAPI a Flask) no requeriría tocar el Dominio.
