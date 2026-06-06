# Documentación del Dominio - to_gcode

Este documento describe el núcleo del sistema, diseñado bajo principios de **DDD (Domain-Driven Design)** y **Arquitectura Limpia**.

## Principios de Diseño
1. **Independencia Tecnológica:** El dominio no conoce bases de datos, frameworks web ni librerías de terceros (svgpathtools, numpy, etc.).
2. **Inmutabilidad:** Los objetos del dominio (Value Objects) son inmutables.
3. **Validación en el Constructor:** Las entidades no pueden existir en un estado inválido.
4. **Terminología 100% Español:** Todo el código fuente utiliza nomenclatura en español.

## Entidades y Value Objects Principales

### Geometría (`src/dominio/entidades/geometria.py`)
- **Punto:** Representa una coordenada (x, y).
- **Trayectoria:** Una secuencia de puntos.
- **Arco:** Representa un arco circular.

### Configuración de Máquina (`src/dominio/entidades/configuracion_maquina.py`)
- **ConfiguracionMaquina:** Define las capacidades físicas (límites, áreas) y el comportamiento de la herramienta.
- **EstadoHerramienta:** Abstracción semántica del estado del cabezal (ARRIBA/ABAJO).

## Servicios de Dominio (`src/dominio/servicios/`)
- **ServicioGeometria:** Lógica compleja de procesamiento geométrico.
- **OptimizadorTrayectoria:** Interfaz de estrategia para algoritmos de optimización de trayectorias.
