from typing import Dict, Any, Optional
from src.aplicacion.limites.puertos_casos_de_uso import PuertoConversionSVG, PuertoConversionImagen, PuertoGestionConfiguracion
from src.adapters.presentadores.presentador_configuracion import PresentadorConfiguracion

class ControladorGCode:
    def __init__(
        self, 
        svg_converter: PuertoConversionSVG, 
        image_converter: PuertoConversionImagen,
        gestor_configuracion: PuertoGestionConfiguracion
    ):
        self.svg_converter = svg_converter
        self.image_converter = image_converter
        self.gestor_configuracion = gestor_configuracion

    def set_config(self, config_data: Dict[str, Any]) -> Dict[str, str]:
        self.gestor_configuracion.guardar(config_data)
        return {"message": "Config saved"}

    def obtener_configuracion(self) -> Optional[Dict[str, Any]]:
        config = self.gestor_configuracion.obtener()
        if not config:
            return None
        return PresentadorConfiguracion.to_http(config)

    def convert_svg(self, svg_content: str) -> Dict[str, str]:
        gcode = self.svg_converter.ejecutar(svg_content)
        return {"gcode": gcode}

    def convert_image(self, image_bytes: bytes) -> Dict[str, str]:
        gcode = self.image_converter.ejecutar(image_bytes)
        return {"gcode": gcode}
