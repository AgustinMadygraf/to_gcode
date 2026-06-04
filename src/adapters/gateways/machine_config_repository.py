from typing import Optional, Dict, Any
from src.application.boundaries.machine_config_repository import MachineConfigRepository
from src.application.boundaries.infrastructure_interfaces import ConfigPersistenceProvider
from src.domain.entities.machine_config import MachineConfig

class SQLAlchemyMachineConfigRepository(MachineConfigRepository):
    """Implementación del repositorio que delega en un proveedor de persistencia."""
    
    def __init__(self, provider: ConfigPersistenceProvider):
        self.provider = provider

    def get_config(self) -> Optional[MachineConfig]:
        data = self.provider.find_first()
        if not data:
            return None
        return MachineConfig(**data)

    def save_config(self, config: MachineConfig) -> None:
        # Tipamos explícitamente el diccionario para satisfacer a Pylance
        data: Dict[str, Any] = {
            "width": config.width,
            "height": config.height,
            "pen_up_command": config.pen_up_command,
            "pen_down_command": config.pen_down_command,
            "feedrate_draw": config.feedrate_draw,
            "feedrate_move": config.feedrate_move,
            "invert_y": config.invert_y,
            "scale_to_fit": config.scale_to_fit
        }
        self.provider.upsert(config.name, data)
