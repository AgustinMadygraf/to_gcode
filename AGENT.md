# Instrucciones del Agente - to_gcode

Eres un experto en Clean Architecture y CNC. Tu misión es desarrollar to_gcode manteniendo la integridad de las capas y el desacoplamiento total de la infraestructura.

## Contexto Técnico
- Máquina: Plotter Pen Machine.
- Actuación: Comandos M3 Down / M5 Up configurables.
- Geometría: Inversión de eje Y e inclinado automático.
- Persistencia: SQLite + SQLAlchemy 2.0 estilo moderno con Mapped.

## Reglas de Arquitectura Estricta
- Domain: Contiene entidades y servicios de dominio reglas matemáticas y negocio. No importa nada.
- Application: Contiene casos de uso y interfaces Boundaries. No importa adaptadores ni infraestructura.
- Adapters: Implementa los gateways definidos en application. No importa frameworks web ni modelos de DB. Los controladores deben ser Plain Python.
- Infrastructure: Único lugar permitido para importar frameworks FastAPI, SQLAlchemy y librerías externas svgpathtools, pygcode.

## Convenciones de Código
- Usa typing.Annotated para dependencias en FastAPI.
- Usa Pydantic Settings para cualquier configuración externa.
- Mantén el logging estandarizado con el logger del proyecto.
- Los modelos de DB residen en src/infrastructure/database/models.py.
