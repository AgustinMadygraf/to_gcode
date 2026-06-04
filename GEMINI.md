# Guía del Proyecto - to_gcode

## Convenciones de Desarrollo
- Arquitectura: Clean Architecture estricta con desacoplamiento de infraestructura.
- Flujo de Dependencias: Domain hacia Application hacia Adapters hacia Infrastructure.

## Estructura de Capas y Reglas
1. Domain: Contiene entidades, Value Objects y servicios de dominio. Es el núcleo puro del sistema.
2. Application: Contiene casos de uso y interfaces llamadas Boundaries.
3. Adapters: 
   - Los Controllers deben ser clases puras de Python.
   - Los Gateways implementan la persistencia y la interacción con librerías de terceros vía wrappers.
4. Infrastructure: Contiene los detalles técnicos FastAPI, SQLAlchemy, wrappers de librerías.

## Estándares Técnicos
- DDD: Priorizar Value Objects para lógica geométrica y entidades ricas.
- SQLAlchemy 2.0: Usa el estilo moderno con Mapped y mapped_column.
- FastAPI: Inyección de dependencias granulares vía Depends.
- Configuración: Centralizada en src/infrastructure/settings/config.py usando Pydantic Settings.
- Tipado: Riguroso para satisfacer a Pylance; usa typing.Annotated y anotaciones explícitas de retorno.
