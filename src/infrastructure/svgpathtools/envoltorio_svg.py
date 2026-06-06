import svgpathtools # type: ignore
import os
from typing import List, Any
from src.adaptadores.pasarelas.envoltorios_tecnicos import EnvoltorioLibreriaSvg
from src.dominio.entidades.geometria import Punto

class SvgTrayectoriaToolsWrapper(EnvoltorioLibreriaSvg):
    def obtener_trayectorias_desde_str(self, contenido_svg: str) -> List[Any]:
        temp_filenombre = "tmp.svg"
        try:
            with open(temp_filenombre, "w") as f:
                f.write(contenido_svg)
            result = svgpathtools.svg2paths(temp_filenombre) # type: ignore
            paths = result[0]
            return list(paths)
        finally:
            if os.path.exists(temp_filenombre):
                os.remove(temp_filenombre)

    def muestrear_trayectoria_a_dominio(self, path: Any, num_muestras: int) -> List[Punto]:
        """Implementación técnica que traduce números complejos a Puntos de dominio."""
        samples = [path.point(i / num_muestras) for i in range(num_muestras + 1)]
        return [Punto(x=float(pos.real), y=float(pos.imag)) for pos in samples]
