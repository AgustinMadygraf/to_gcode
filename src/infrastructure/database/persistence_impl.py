from typing import Optional, Dict, Any
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from src.adaptadores.pasarelas.envoltorios_tecnicos import ProveedorPersistenciaConfiguracion
from src.infrastructure.database.models import ConfiguracionMaquinaModel
from src.infrastructure.settings.logger import logger

class SQLAlchemyConfigProvider(ProveedorPersistenciaConfiguracion):
    def __init__(self, session: Session):
        self.session = session

    def buscar_primero(self) -> Optional[Dict[str, Any]]:
        logger.debug("Fetching first machine configuration from datosbase.")
        stmt = select(ConfiguracionMaquinaModel)
        # Usamos .first() para evitar excepciones si hay múltiples configuraciones por error
        model = self.session.execute(stmt).scalars().first()
        
        if not model:
            return None
            
        return {
            "nombre": model.nombre,
            "width": model.width,
            "height": model.height,
            "max_x": model.max_x,
            "max_y": model.max_y,
            "pen_up_comando": model.pen_up_comando,
            "pen_down_comando": model.pen_down_comando,
            "feedrate_draw": model.feedrate_draw,
            "feedrate_move": model.feedrate_move,
            "invert_y": model.invert_y,
            "scale_to_fit": model.scale_to_fit
        }

    def actualizar_o_insertar(self, nombre: str, datos: Dict[str, Any]) -> None:
        logger.info(f"Upserting configuration for: {nombre}")
        stmt = select(ConfiguracionMaquinaModel).filter_by(nombre=nombre)
        model = self.session.execute(stmt).scalars().first()
        
        if model:
            logger.debug(f"Updating existing record for {nombre}.")
            update_stmt = update(ConfiguracionMaquinaModel).where(ConfiguracionMaquinaModel.nombre == nombre).values(**datos)
            self.session.execute(update_stmt)
        else:
            logger.debug(f"Creating new record for {nombre}.")
            new_model = ConfiguracionMaquinaModel(nombre=nombre, **datos)
            self.session.add(new_model)
        self.session.commit()
