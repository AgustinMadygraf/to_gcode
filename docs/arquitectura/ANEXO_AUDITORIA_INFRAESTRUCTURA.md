# Auditoría de Infraestructura (`src/infrastructure`)

Este documento registra los hallazgos de la auditoría arquitectónica realizada sobre la capa de infraestructura del proyecto `to_gcode`.

## Objetivo
Evaluar el acoplamiento técnico, la adherencia a la Clean Architecture y los trade-offs de rendimiento en los componentes de infraestructura.

## Hallazgos Clave

### 1. Aislamiento de Librerías Externas
- **Componente:** `src/infrastructure/numpy/skeleton_wrapper.py` y `src/infrastructure/image_processing/raster_wrapper.py`
- **Observación:** Existe un acoplamiento inevitable con `numpy` y `scikit-image` debido a que el procesamiento de imágenes requiere manipular estructuras de datos masivas.
- **Justificación:** Se ha decidido mantener el paso de objetos `np.ndarray` a través de los wrappers de infraestructura para evitar copias costosas de memoria (clonación de matrices).
- **Decisión de Diseño:** La lógica de negocio (casos de uso) queda protegida gracias a la abstracción definida por la interfaz `AbstraccionEsqueleto` (en `src/adaptadores/pasarelas/envoltorios_tecnicos.py`). Esta interfaz es agnóstica a cualquier librería externa.

### 2. Capa de Persistencia
- **Componente:** `src/infrastructure/database/`
- **Observación:** Separación clara entre `ConfiguracionMaquina` (Dominio) y `ConfiguracionMaquinaModel` (SQLAlchemy).
- **Justificación:** Permite la evolución independiente del modelo de base de datos y la entidad de dominio.

### 3. Inyección de Dependencias
- **Componente:** `src/infrastructure/fastapi/dependencies.py`
- **Observación:** Se utiliza un patrón de factoría explícito que cumple con la Inversión de Dependencias (DIP).
- **Justificación:** La arquitectura es robusta y los casos de uso dependen exclusivamente de interfaces (puertos), garantizando desacoplamiento.

### 4. Recomendaciones Finales
- **Seguridad de Tipos:** Se ha confirmado con `mypy` que las interfaces son respetadas.
- **Mantenimiento:** La estructura actual de carpetas es robusta. No se recomienda reestructuración, sino mantener la disciplina de no filtrar tipos de librerías externas fuera de las clases de infraestructura (wrappers).

---
*Fecha de auditoría: 6 de junio de 2026*
*Estado: Arquitectura validada y estable.*
