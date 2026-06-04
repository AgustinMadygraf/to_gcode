"""
Path: src/infrastructure/svgpathtools/wrapper.py
"""

import svgpathtools # type: ignore
import os
from typing import List, Any
from src.application.boundaries.infrastructure_interfaces import SvgLibraryWrapper

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

    def sample_path(self, path: Any, num_samples: int) -> List[complex]:
        return [path.point(i / num_samples) for i in range(num_samples + 1)]
