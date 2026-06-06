# to_gcode

MVP para convertir archivos SVG a formato GCode para plotters, diseñado bajo principios de **Arquitectura Limpia** y **DDD**.

## Guía de Desarrollo
El proyecto sigue una estructura estricta de capas para garantizar la independencia tecnológica:
1. **Dominio**: Núcleo puro del sistema (entidades y reglas de negocio).
2. **Aplicación**: Casos de uso y orquestación.
3. **Adaptadores**: Puentes entre el dominio/aplicación y los detalles técnicos.
4. **Infraestructura**: Implementaciones concretas (FastAPI, librerías externas, persistencia).

## Ejecución
1. Crear entorno virtual y activar.
2. Instalar dependencias: `pip install -r requirements.txt`
3. Ejecutar: `./run.sh`
4. El backend estará disponible en `http://localhost:8000`.
5. Abrir `frontend/index.html` en tu navegador.

## Documentación Técnica
Consulta la carpeta `docs/` para obtener detalles sobre la arquitectura, la API y los protocolos de integración.
