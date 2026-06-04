# TODO - to_gcode

## Fase 1: Documentación y Arquitectura
- [x] Definir alcance MVP (M3/M5).
- [x] Refactor a Clean Architecture (Carpetas: domain, application, adapters, infrastructure).
- [x] Sincronizar archivos de gobernanza (README, GEMINI, AGENT, SRS).

## Fase 2: Definición de Entidades y Contratos
- [ ] Crear entidades en `domain/entities/`: `MachineConfig`, `Path`, `Point` (LISTO PARA INICIAR): `MachineConfig`, `Path`, `Point`.
- [ ] Definir contratos en `application/contracts/`: `MachineConfigRepository`, `VectorParser`, `GCodeGenerator`.

## Fase 3: Persistencia e Infraestructura Inicial
- [ ] Configurar SQLAlchemy y modelo de DB en `infrastructure/database/`.
- [ ] Implementar `SQLAlchemyMachineConfigRepository` en `adapters/repositories/`.

## Fase 4: Implementación de Casos de Uso
- [ ] Implementar caso de uso `GetMachineConfig`.
- [ ] Implementar caso de uso `ConvertSVGToGCode`.

## Fase 5: Adaptadores Externos y API
- [ ] Implementar `SvgPathToolsParser` en `adapters/gateways/`.
- [ ] Implementar `PyGCodeGenerator` en `adapters/gateways/`.
- [ ] Crear controladores y rutas FastAPI en `infrastructure/api/`.
