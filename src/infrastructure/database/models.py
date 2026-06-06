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

class ConfiguracionMaquinaModel(Base):
    __tablename__ = "machine_configs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    ancho_area_trabajo: Mapped[float] = mapped_column(Float)
    alto_area_trabajo: Mapped[float] = mapped_column(Float)
    ancho_maximo_maquina: Mapped[float] = mapped_column(Float, default=0.0)
    alto_maximo_maquina: Mapped[float] = mapped_column(Float, default=0.0)
    comando_pluma_arriba: Mapped[str] = mapped_column(String(20))
    comando_pluma_abajo: Mapped[str] = mapped_column(String(20))
    velocidad_dibujo: Mapped[float] = mapped_column(Float)
    velocidad_movimiento: Mapped[float] = mapped_column(Float)
    invertir_eje_y: Mapped[bool] = mapped_column(Boolean, default=True)
    ajustar_a_escala: Mapped[bool] = mapped_column(Boolean, default=True)

def init_db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    if session.query(ConfiguracionMaquinaModel).count() == 0:
        default_config = ConfiguracionMaquinaModel(
            nombre="default",
            ancho_area_trabajo=210.0,
            alto_area_trabajo=297.0,
            ancho_maximo_maquina=210.0,
            alto_maximo_maquina=297.0,
            comando_pluma_arriba="M5",
            comando_pluma_abajo="M3",
            velocidad_dibujo=100.0,
            velocidad_movimiento=500.0,
            invertir_eje_y=True,
            ajustar_a_escala=True
        )
        session.add(default_config)
        session.commit()
    session.close()
