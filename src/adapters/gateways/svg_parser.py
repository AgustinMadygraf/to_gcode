"""
Path: src/adapters/gateways/svg_parser.py
"""

from typing import List
from src.application.boundaries.gateways import VectorParser
from src.application.boundaries.infrastructure_interfaces import SvgLibraryWrapper
from src.domain.entities.machine_config import Path as DomainPath, Point

class SvgPathToolsParser(VectorParser):
    def __init__(self, wrapper: SvgLibraryWrapper):
        self.wrapper = wrapper

    def parse_svg(self, svg_content: str) -> List[DomainPath]:
        paths = self.wrapper.get_paths_from_str(svg_content)
        
        domain_paths: List[DomainPath] = []
        for path in paths:
            points: List[Point] = []
            NUM_SAMPLES = 50 
            samples = self.wrapper.sample_path(path, NUM_SAMPLES)
            for pos in samples:
                points.append(Point(x=float(pos.real), y=float(pos.imag)))
            domain_paths.append(DomainPath(points=points))
        return domain_paths
