"""
Trayectoria: src/infrastructure/database/session_provider.py
"""

from typing import Generator, Any
from src.application.boundaries.infrastructure_interfaces import DatabaseSessionProvider
from src.infrastructure.database.models import SessionLocal

class SqlAlchemySessionProvider(DatabaseSessionProvider):
    def get_session(self) -> Generator[Any, None, None]:
        session = SessionLocal()
        try:
            yield session
        finally:
            session.close()
