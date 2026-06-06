import svgpathtools # type: ignore
import os
from typing import List, Any
from src.application.boundaries.infrastructure_interfaces import SvgLibraryWrapper
from src.domain.entities.geometria import Punto

class SvgTrayectoriaToolsWrapper(SvgLibraryWrapper):
    def get_paths_from_str(self, svg_content: str) -> List[Any]:
        temp_filename = "tmp.svg"
        try:
            with open(temp_filename, "w") as f:
                f.write(svg_content)
            result = svgpathtools.svg2paths(temp_filename) # type: ignore
            paths = result[0]
            return list(paths)
        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

    def sample_path_to_domain(self, path: Any, num_samples: int) -> List[Punto]:
        """Implementación técnica que traduce números complejos a Puntos de dominio."""
        samples = [path.point(i / num_samples) for i in range(num_samples + 1)]
        return [Punto(x=float(pos.real), y=float(pos.imag)) for pos in samples]
