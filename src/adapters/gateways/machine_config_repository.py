"""
Trayectoria: src/adapters/gateways/machine_config_repository.py
"""
from typing import Optional, Dict, Any
from src.application.boundaries.machine_config_repository import ConfiguracionMaquinaRepository
from src.application.boundaries.infrastructure_interfaces import ConfigPersistenceProvider
from src.domain.entities.configuracion_maquina import ConfiguracionMaquina

class SQLAlchemyConfiguracionMaquinaRepository(ConfiguracionMaquinaRepository):
    def __init__(self, provider: ConfigPersistenceProvider):
        self.provider = provider

    def get_config(self) -> Optional[ConfiguracionMaquina]:
        data = self.provider.find_first()
        if not data:
            return None

        if 'max_x' not in data:
            data['max_x'] = data.get('width', 0.0)
        if 'max_y' not in data:
            data['max_y'] = data.get('height', 0.0)
            
        return ConfiguracionMaquina(**data)

    def save_config(self, config: ConfiguracionMaquina) -> None:
        data: Dict[str, Any] = {
            "width": config.width,
            "height": config.height,
            "max_x": config.max_x,
            "max_y": config.max_y,
            "pen_up_command": config.pen_up_command,
            "pen_down_command": config.pen_down_command,
            "feedrate_draw": config.feedrate_draw,
            "feedrate_move": config.feedrate_move,
            "invert_y": config.invert_y,
            "scale_to_fit": config.scale_to_fit
        }
        self.provider.upsert(config.name, data)
