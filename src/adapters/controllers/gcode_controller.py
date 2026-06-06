"""
Path: src/adapters/controllers/gcode_controller.py
"""

from typing import Dict, Any, Optional
from src.aplicacion.casos_de_uso.convertir_svg import ConvertirSVGAGCode
from src.aplicacion.casos_de_uso.convertir_imagen import ConvertirImagenAGCode
from src.aplicacion.limites.interfaz_repositorio_configuracion_maquina import RepositorioConfiguracionMaquina
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina
from src.adapters.presenters.config_presenter import ConfigPresenter

class GCodeController:
    def __init__(
        self, 
        svg_converter: ConvertirSVGAGCode, 
        image_converter: ConvertirImagenAGCode,
        repositorio: RepositorioConfiguracionMaquina
    ):
        self.svg_converter = svg_converter
        self.image_converter = image_converter
        self.repositorio = repositorio

    def set_config(self, config_data: Dict[str, Any]) -> Dict[str, str]:
        entity = ConfiguracionMaquina(**config_data)
        self.repositorio.guardar_configuracion(entity)
        return {"message": "Config saved"}

    def obtener_configuracion(self) -> Optional[Dict[str, Any]]:
        config = self.repositorio.obtener_configuracion()
        if not config:
            return None
        return ConfigPresenter.to_http(config)

    def convert_svg(self, svg_content: str) -> Dict[str, str]:
        gcode = self.svg_converter.ejecutar(svg_content)
        return {"gcode": gcode}

    def convert_image(self, image_bytes: bytes) -> Dict[str, str]:
        gcode = self.image_converter.ejecutar(image_bytes)
        return {"gcode": gcode}
