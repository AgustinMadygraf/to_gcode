from typing import Dict, Any
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina

class PresentadorConfiguracion:
    @staticmethod
    def a_http(config: ConfiguracionMaquina) -> Dict[str, Any]:
        return {
            "nombre": config.nombre,
            "dimensiones": {
                "ancho": config.ancho_area_trabajo,
                "alto": config.alto_area_trabajo
            },
            "limites": {
                "max_x": config.ancho_maximo_maquina,
                "max_y": config.alto_maximo_maquina
            },
            "comandos": {
                "arriba": config.comando_pluma_arriba,
                "abajo": config.comando_pluma_abajo
            },
            "velocidades": {
                "dibujo": config.velocidad_dibujo,
                "movimiento": config.velocidad_movimiento
            },
            "opciones": {
                "invertir_y": config.invertir_eje_y,
                "ajustar_a_escala": config.ajustar_a_escala
            }
        }
