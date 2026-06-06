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
    width: Mapped[float] = mapped_column(Float)
    height: Mapped[float] = mapped_column(Float)
    max_x: Mapped[float] = mapped_column(Float, default=0.0)
    max_y: Mapped[float] = mapped_column(Float, default=0.0)
    pen_up_comando: Mapped[str] = mapped_column(String(20))
    pen_down_comando: Mapped[str] = mapped_column(String(20))
    feedrate_draw: Mapped[float] = mapped_column(Float)
    feedrate_move: Mapped[float] = mapped_column(Float)
    invert_y: Mapped[bool] = mapped_column(Boolean, default=True)
    scale_to_fit: Mapped[bool] = mapped_column(Boolean, default=True)

def init_db():
    Base.metadata.create_all(bind=engine)
    # Seed default config if empty
    session = SessionLocal()
    if session.query(ConfiguracionMaquinaModel).count() == 0:
        default_config = ConfiguracionMaquinaModel(
            nombre="default",
            width=210.0,
            height=297.0,
            max_x=210.0,
            max_y=297.0,
            pen_up_comando="M5",
            pen_down_comando="M3",
            feedrate_draw=100.0,
            feedrate_move=500.0,
            invert_y=True,
            scale_to_fit=True
        )
        session.add(default_config)
        session.commit()
    session.close()
