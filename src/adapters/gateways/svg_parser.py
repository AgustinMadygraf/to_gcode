from typing import List
from src.application.boundaries.gateways import VectorParser
from src.application.boundaries.infrastructure_interfaces import SvgLibraryWrapper
from src.domain.entities.geometry import Path as DomainPath

class SvgPathToolsParser(VectorParser):
    def __init__(self, wrapper: SvgLibraryWrapper, sampling_resolution: int = 50):
        self.wrapper = wrapper
        self.sampling_resolution = sampling_resolution

    def parse_svg(self, svg_content: str) -> List[DomainPath]:
        try:
            paths = self.wrapper.get_paths_from_str(svg_content)
        except Exception as e:
            raise ValueError(f"Failed to parse SVG: {str(e)}")
        
        domain_paths: List[DomainPath] = []
        for path in paths:
            # El adaptador ya no sabe que existen números complejos
            points = self.wrapper.sample_path_to_domain(path, self.sampling_resolution)
            domain_paths.append(DomainPath(points=points))
        return domain_paths
