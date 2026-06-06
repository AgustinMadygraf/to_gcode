from typing import Dict, Any, Optional
from src.application.use_cases.convert_svg import ConvertSVGToGCode
from src.application.use_cases.convert_image import ConvertImageToGCode
from src.application.boundaries.machine_config_repository import ConfiguracionMaquinaRepository
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina
from src.adapters.presenters.config_presenter import ConfigPresenter

class GCodeController:
    """
    Controlador de Excelencia Técnica. 
    Agnóstico a librerías, formatos de salida complejos y normalización técnica.
    """
    def __init__(
        self, 
        svg_converter: ConvertSVGToGCode, 
        image_converter: ConvertImageToGCode,
        repo: ConfiguracionMaquinaRepository
    ):
        self.svg_converter = svg_converter
        self.image_converter = image_converter
        self.repo = repo

    def set_config(self, config_data: Dict[str, Any]) -> Dict[str, str]:
        entity = ConfiguracionMaquina(**config_data)
        self.repo.save_config(entity)
        return {"message": "Config saved"}

    def get_config(self) -> Optional[Dict[str, Any]]:
        config = self.repo.get_config()
        if not config:
            return None
        
        # Delegamos el formateo al Presenter
        return ConfigPresenter.to_http(config)

    def convert_svg(self, svg_content: str) -> Dict[str, str]:
        gcode = self.svg_converter.execute(svg_content)
        return {"gcode": gcode}

    def convert_image(self, image_bytes: bytes) -> Dict[str, str]:
        gcode = self.image_converter.execute(image_bytes)
        return {"gcode": gcode}
