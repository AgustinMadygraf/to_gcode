from typing import List
from src.aplicacion.limites.puertos import AnalizadorVectorial
from src.adapters.pasarelas.envoltorios_tecnicos import EnvoltorioLibreriaSvg
from src.dominio.entidades.geometria import Trayectoria as DomainTrayectoria

class SvgTrayectoriaToolsParser(AnalizadorVectorial):
    def __init__(self, wrapper: EnvoltorioLibreriaSvg, sampling_resolution: int = 50):
        self.wrapper = wrapper
        self.sampling_resolution = sampling_resolution

    def parsear_svg(self, svg_content: str) -> List[DomainTrayectoria]:
        try:
            paths = self.wrapper.obtener_trayectorias_desde_str(svg_content)
        except Exception as e:
            raise ValueError(f"Failed to parse SVG: {str(e)}")
        
        domain_paths: List[DomainTrayectoria] = []
        for path in paths:
            # El adaptador ya no sabe que existen números complejos
            points = self.wrapper.muestrear_trayectoria_a_dominio(path, self.sampling_resolution)
            domain_paths.append(DomainTrayectoria(puntos=points))
        return domain_paths
