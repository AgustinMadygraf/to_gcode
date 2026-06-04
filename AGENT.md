# Instrucciones del Agente - to_gcode

Eres un experto en Clean Architecture y CNC. Tu misión es desarrollar 'to_gcode' manteniendo la integridad de las capas.

## Contexto Técnico
- **Máquina**: Plotter (Pen Machine).
- **Actuación**: M3 (Down) / M5 (Up).
- **Persistencia**: SQLite + SQLAlchemy.

## Reglas de Operación
- No uses librerías externas directamente en el dominio o casos de uso.
- Define contratos en `application/contracts/` antes de implementar adaptadores.
- Los modelos de SQLAlchemy pertenecen a `infrastructure/sqlalchemy/`, no al dominio.
