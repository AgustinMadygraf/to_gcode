# TODO - to_gcode

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

## Fase 5: Fronend con HTML, Bootstrap (CSS) y JS

## Fase 6: Validación y Calidad (ENFOQUE ACTUAL)
- [ ] Implementar Unit Tests para GeometryService.
- [ ] Implementar Unit Tests para Casos de Uso.
- [ ] Implementar Tests de Integración para la API.
- [ ] Validar con SVG reales y simulador de G-code.

## Fase 7: Evolución (V2.0)
- [ ] Implementar Path Ordering (Optimización de saltos de pen).
- [ ] Soporte para múltiples capas/colores.
