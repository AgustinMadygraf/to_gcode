"""
Path: src/adaptadores/presentadores/presentador_configuracion.py
"""

from typing import Dict, Any
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina

class PresentadorConfiguracion:
    """Encargado de formatear la salida de configuración para el cliente (API/UI)."""
    
    @staticmethod
    def a_http(config: ConfiguracionMaquina) -> Dict[str, Any]:
        return {
            "nombre": config.name,
            "dimensiones": {
                "ancho": config.width,
                "alto": config.height
            },
            "limites": {
                "max_x": config.max_x,
                "max_y": config.max_y
            },
            "comandos": {
                "arriba": config.pen_up_command,
                "abajo": config.pen_down_command
            },
            "velocidades": {
                "dibujo": config.feedrate_draw,
                "movimiento": config.feedrate_move
            },
            "opciones": {
                "invertir_y": config.invert_y,
                "ajustar_a_escala": config.scale_to_fit
            }
        }
