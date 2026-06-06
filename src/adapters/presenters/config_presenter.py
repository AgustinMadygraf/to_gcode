from typing import Dict, Any
from src.domain.entities.configuracion_maquina import ConfiguracionMaquina

class ConfigPresenter:
    """Encargado de formatear la salida de configuración para el cliente (API/UI)."""
    
    @staticmethod
    def to_http(config: ConfiguracionMaquina) -> Dict[str, Any]:
        """Convierte la entidad a un formato amigable para JSON/HTTP."""
        return {
            "name": config.name,
            "dimensions": {
                "width": config.width,
                "height": config.height
            },
            "limits": {
                "max_x": config.max_x,
                "max_y": config.max_y
            },
            "commands": {
                "up": config.pen_up_command,
                "down": config.pen_down_command
            },
            "speeds": {
                "draw": config.feedrate_draw,
                "move": config.feedrate_move
            },
            "options": {
                "invert_y": config.invert_y,
                "scale_to_fit": config.scale_to_fit
            }
        }
