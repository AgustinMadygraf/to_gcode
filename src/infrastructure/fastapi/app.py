"""
Path: src/infrastructure/fastapi/app.py
"""

from typing import Dict, Any
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.fastapi.routes import router as gcode_router
from src.infrastructure.database.models import init_db
from src.infrastructure.settings.config import settings
from src.infrastructure.settings.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database...")
    init_db()
    logger.info("Application startup complete.")
    yield
    logger.info("Application shutdown.")

app = FastAPI(
    title=settings.APP_TITLE, 
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# Configuración de CORS usando settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    logger.warning(f"Value Error: {exc}")
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )

@app.exception_handler(TypeError)
async def type_error_handler(request: Request, exc: TypeError) -> JSONResponse:
    logger.error(f"Type Error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": f"Data error: {str(exc)}"},
    )

@app.get("/")
def health_check() -> Dict[str, Any]:
    return {
        "status": "online", 
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG
    }

app.include_router(gcode_router)
