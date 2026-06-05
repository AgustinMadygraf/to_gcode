import svgpathtools # type: ignore
import os
from typing import List, Any
from src.application.boundaries.infrastructure_interfaces import SvgLibraryWrapper
from src.domain.entities.geometry import Point

class SvgPathToolsWrapper(SvgLibraryWrapper):
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

    def sample_path_to_domain(self, path: Any, num_samples: int) -> List[Point]:
        """Implementación técnica que traduce números complejos a Points de dominio."""
        samples = [path.point(i / num_samples) for i in range(num_samples + 1)]
        return [Point(x=float(pos.real), y=float(pos.imag)) for pos in samples]
