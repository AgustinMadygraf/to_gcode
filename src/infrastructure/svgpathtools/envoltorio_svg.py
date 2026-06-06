"""
Path: src/infrastructure/svgpathtools/envoltorio_svg.py
"""

import svgpathtools # type: ignore
import io
from typing import List, Any
from src.adaptadores.pasarelas.envoltorios_tecnicos import EnvoltorioLibreriaSvg
from src.dominio.entidades.geometria import Punto

class SvgTrayectoriaToolsWrapper(EnvoltorioLibreriaSvg):
    def obtener_trayectorias_desde_str(self, contenido_svg: str) -> List[Any]:
        f = io.StringIO(contenido_svg)
        result = svgpathtools.svg2paths(f) # type: ignore
        paths = result[0]
        return list(paths)

    def muestrear_trayectoria_a_dominio(self, trayectoria: Any, num_muestras: int) -> List[Punto]:
        samples = [trayectoria.point(i / num_muestras) for i in range(num_muestras + 1)]
        return [Punto(x=float(pos.real), y=float(pos.imag)) for pos in samples]
