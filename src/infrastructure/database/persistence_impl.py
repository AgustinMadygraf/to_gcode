"""
Path: src/infrastructure/database/persistence_impl.py
"""

from typing import Optional, Dict, Any
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from src.application.boundaries.infrastructure_interfaces import ConfigPersistenceProvider
from src.infrastructure.database.models import MachineConfigModel
from src.infrastructure.settings.logger import logger

class SQLAlchemyConfigProvider(ConfigPersistenceProvider):
    def __init__(self, session: Session):
        self.session = session

    def find_first(self) -> Optional[Dict[str, Any]]:
        logger.debug("Fetching first machine configuration from database.")
        stmt = select(MachineConfigModel)
        model = self.session.execute(stmt).scalar_one_or_none()
        
        if not model:
            return None
            
        # Convertimos el modelo a dict de forma explícita
        return {
            "name": model.name,
            "width": model.width,
            "height": model.height,
            "pen_up_command": model.pen_up_command,
            "pen_down_command": model.pen_down_command,
            "feedrate_draw": model.feedrate_draw,
            "feedrate_move": model.feedrate_move,
            "invert_y": model.invert_y,
            "scale_to_fit": model.scale_to_fit
        }

    def upsert(self, name: str, data: Dict[str, Any]) -> None:
        logger.info(f"Upserting configuration for: {name}")
        stmt = select(MachineConfigModel).filter_by(name=name)
        model = self.session.execute(stmt).scalar_one_or_none()
        
        if model:
            logger.debug(f"Updating existing record for {name}.")
            # Usar update directo es más eficiente y seguro
            update_stmt = update(MachineConfigModel).where(MachineConfigModel.name == name).values(**data)
            self.session.execute(update_stmt)
        else:
            logger.debug(f"Creating new record for {name}.")
            new_model = MachineConfigModel(name=name, **data)
            self.session.add(new_model)
        self.session.commit()
