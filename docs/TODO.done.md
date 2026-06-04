# TODO - to_gcode (MVP FINALIZADO)

## Fase 1: Documentación y Arquitectura
- [x] Definir alcance MVP (M3/M5).
- [x] Refactor a Clean Architecture (Domain, Application, Adapters, Infrastructure).
- [x] Sincronizar archivos de gobernanza (GEMINI.md, AGENT.md).

## Fase 2: Núcleo del Sistema (Domain & Application)
- [x] Crear entidades (MachineConfig, Point, Path).
- [x] Implementar Servicio de Dominio (GeometryService) para transformaciones.
- [x] Definir interfaces (Boundaries) para desacoplamiento total.
- [x] Implementar caso de uso ConvertSVGToGCode.

## Fase 3: Persistencia e Infraestructura
- [x] Configurar SQLAlchemy 2.0 (Mapped/mapped_column).
- [x] Implementar Gateway de persistencia desacoplado (PersistenceProvider).
- [x] Configuración centralizada (.env, Pydantic Settings).
- [x] Sistema de Logging estandarizado.

## Fase 4: Adaptadores y API
- [x] Implementar Wrappers de infraestructura (svgpathtools, pygcode).
- [x] Implementar Gateways agnósticos (Parser, Generator).
- [x] Desacoplar Controlador de frameworks web (GCodeController puro).
- [x] Implementar rutas FastAPI con Inyección de Dependencias (Depends).
- [x] Implementar Exception Handlers globales y CORS.

## Fase 5: Validación y Calidad
- [x] Unit Tests: GeometryService.
- [x] Unit Tests: Casos de Uso.
- [x] Unit Tests: Adaptadores (Controllers & Repositorios).
- [x] Tests de Integración: API (/convert).
- [x] Tests de Integración: API (/config).

## Fase 6: Documentación API
- [x] Crear docs/API.md (Narrativa).
- [x] Validar autogeneración Swagger/ReDoc.
