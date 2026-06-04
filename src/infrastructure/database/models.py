"""
Path: src/infrastructure/database/models.py
"""

from sqlalchemy import create_engine, String, Float, Boolean
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from src.infrastructure.settings.config import settings

engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class MachineConfigModel(Base):
    __tablename__ = "machine_configs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    width: Mapped[float] = mapped_column(Float)
    height: Mapped[float] = mapped_column(Float)
    pen_up_command: Mapped[str] = mapped_column(String)
    pen_down_command: Mapped[str] = mapped_column(String)
    feedrate_draw: Mapped[float] = mapped_column(Float)
    feedrate_move: Mapped[float] = mapped_column(Float)
    invert_y: Mapped[bool] = mapped_column(Boolean, default=True)
    scale_to_fit: Mapped[bool] = mapped_column(Boolean, default=True)

def init_db():
    Base.metadata.create_all(bind=engine)
