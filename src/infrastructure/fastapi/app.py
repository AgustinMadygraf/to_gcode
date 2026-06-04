"""
Path: src/infrastructure/fastapi/app.py
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.infrastructure.fastapi.routes import router as gcode_router
from src.infrastructure.database.models import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="to_gcode API", 
    description="Conversor de SVG a G-code para Plotters (Clean Architecture)",
    lifespan=lifespan
)

app.include_router(gcode_router)
