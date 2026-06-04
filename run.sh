#!/bin/bash

# Activar entorno virtual si existe
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Asegurar que las dependencias estén instaladas
pip install -q fastapi uvicorn sqlalchemy svgpathtools pygcode python-multipart pydantic-settings

# Servir el frontend y el backend
echo "Iniciando to_gcode MVP..."
echo "Backend: http://localhost:8000"
echo "Frontend: abre 'frontend/index.html' en tu navegador."

# Ejecutar el servidor uvicorn
export PYTHONPATH=$PYTHONPATH:.
uvicorn src.infrastructure.fastapi.app:app --reload --host 0.0.0.0 --port 8000
