"""
Path: src/adaptadores/controladores/controlador_codigo_g.py
"""

from typing import Dict, Any, Optional
from src.aplicacion.limites.puertos_casos_de_uso import PuertoConversionSVG, PuertoConversionImagen, PuertoGestionConfiguracion
from src.adaptadores.presentadores.presentador_configuracion import PresentadorConfiguracion

class ControladorCodigoG:
    def __init__(
        self, 
        conversor_svg: PuertoConversionSVG, 
        conversor_imagen: PuertoConversionImagen,
        gestor_configuracion: PuertoGestionConfiguracion
    ):
        self.conversor_svg = conversor_svg
        self.conversor_imagen = conversor_imagen
        self.gestor_configuracion = gestor_configuracion

    def establecer_configuracion(self, config_data: Dict[str, Any]) -> Dict[str, str]:
        self.gestor_configuracion.guardar(config_data)
        return {"mensaje": "Configuración guardada"}

    def obtener_configuracion(self) -> Optional[Dict[str, Any]]:
        config = self.gestor_configuracion.obtener()
        if not config:
            return None
        return PresentadorConfiguracion.a_http(config)

    def convertir_svg(self, svg_content: str) -> Dict[str, str]:
        gcode = self.conversor_svg.ejecutar(svg_content)
        return {"gcode": gcode}

    def convertir_imagen(self, image_bytes: bytes) -> Dict[str, str]:
        gcode = self.conversor_imagen.ejecutar(image_bytes)
        return {"gcode": gcode}
