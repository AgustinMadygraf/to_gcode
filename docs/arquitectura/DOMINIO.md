# Documentación del Dominio - to_gcode

Este documento describe el núcleo del sistema, diseñado bajo principios de **DDD (Domain-Driven Design)** y **Arquitectura Limpia**.

## Principios de Diseño
1. **Independencia Tecnológica:** El dominio no conoce bases de datos, frameworks web ni librerías de terceros (svgpathtools, numpy, etc.).
2. **Inmutabilidad:** Los objetos del dominio (Value Objects) son inmutables para garantizar la seguridad de hilos y evitar efectos secundarios.
3. **Validación en el Constructor:** Las entidades no pueden existir en un estado inválido.
4. **Tipado Riguroso:** Se evita el uso de `Any` y diccionarios genéricos en favor de tipos explícitos.

## Entidades y Value Objects Principales

### Geometría (src/domain/entities/geometry.py)
- **Point:** Representa una coordenada (x, y) con capacidad de cálculo de distancias.
- **Path:** Una secuencia de puntos. Evolucionando hacia una estructura de segmentos polimórficos.
- **Arc:** Representa un arco circular con centro, radio y puntos de control.
- **Rect:** Bounding Box para cálculos de escalado y encuadre.

### Configuración de Máquina (src/domain/entities/machine_config.py)
- **MachineConfig:** Define las capacidades físicas (límites, áreas) y el comportamiento de la herramienta.
- **ToolState (Próximamente):** Abstracción semántica del estado del cabezal (UP/DOWN) para desacoplar el dominio de la sintaxis G-Code.

## Servicios de Dominio (src/domain/services/)
- **GeometryService:** Lógica compleja de procesamiento geométrico (ajuste de arcos, simplificación).
- **PathOptimizer:** Interfaz de estrategia para algoritmos de optimización de trayectorias (Greedy, TSP, etc.).

## Próximas Mejoras (Blindaje Nivel Industrial)
- Implementación de **Segmentos Polimórficos** (LineTo, ArcTo) en lugar de listas de puntos crudas.
- Desacoplamiento total de comandos de texto (M3/M5) en favor de **Estados de Herramienta**.
- Validación de **Consistencia Física** entre dimensiones de área y límites de hardware.
