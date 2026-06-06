"""
Trayectoria: src/infrastructure/database/session_provider.py
"""

from typing import Generator, Any
from src.aplicacion.limites.interfaces_infraestructura import ProveedorSesionBaseDatos
from src.infrastructure.database.models import SessionLocal

class SqlAlchemySessionProvider(ProveedorSesionBaseDatos):
    def obtener_sesion(self) -> Generator[Any, None, None]:
        session = SessionLocal()
        try:
            yield session
        finally:
            session.close()
