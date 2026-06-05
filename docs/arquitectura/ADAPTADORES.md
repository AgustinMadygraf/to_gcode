# Capa de Adaptadores (Interface Adapters) - to_gcode

Esta capa actúa como el puente de comunicación entre el mundo exterior (Infraestructura) y el núcleo del sistema (Dominio y Aplicación). Su responsabilidad es la traducción bidireccional de datos.

## Principios de Diseño
1. **Traductores Pasivos:** Los adaptadores no deben contener lógica de negocio ni de orquestación compleja.
2. **Agnosticismo Técnico:** Los adaptadores no dependen de las estructuras de datos internas de las librerías de infraestructura (DIP).
3. **Responsabilidad Única:** Separación clara entre entrada (Controllers), salida (Presenters) e interacción con servicios externos (Gateways).

## Componentes Principales

### 1. Controllers (src/adapters/controllers/)
- **GCodeController:** Recibe peticiones de la API o CLI. Su única función es transformar el payload técnico en entidades o parámetros de dominio y llamar al caso de uso correspondiente. No realiza validaciones de negocio ni normalizaciones de datos.

### 2. Gateways (src/adapters/gateways/)
- **SvgPathToolsParser:** Implementa `VectorParser`. Traduce el contenido SVG a trayectorias de dominio. Utiliza un contrato de Wrapper que devuelve tipos de dominio (`Point`), aislando al adaptador de la implementación técnica (ej. números complejos).
- **PyGCodeGenerator:** Implementa `GCodeGenerator`. Traduce trayectorias y configuraciones de dominio a sintaxis G-Code. No realiza procesamiento geométrico; recibe datos ya simplificados y listos para el trazo.
- **SQLAlchemyMachineConfigRepository:** Implementa la persistencia. Mapea modelos de base de datos a entidades de dominio.

### 3. Presenters (src/adapters/presenters/)
- **ConfigPresenter:** Encapsula la lógica de formateo de salida. Toma una entidad `MachineConfig` y construye la estructura de datos (DTO) requerida por el cliente final (ej. agrupando dimensiones, límites y velocidades en objetos anidados para una API REST).

## Desacoplamiento via DIP
Los adaptadores interactúan con la infraestructura a través de interfaces definidas en la capa de aplicación (`infrastructure_interfaces.py`). Esto permite que el sistema sea inmune a cambios en las librerías externas. Por ejemplo, si se cambia la librería de procesamiento SVG, solo se modifica el Wrapper en Infraestructura; el Adaptador permanece intacto.

## Flujo de Traducción
- **Entrada:** `JSON/Binary` -> `Schema (Infra)` -> `Dict/DTO` -> `Adaptador` -> `Entidad (Dominio)`
- **Salida:** `Entidad (Dominio)` -> `Adaptador` -> `Presenter` -> `JSON/Response (Infra)`
