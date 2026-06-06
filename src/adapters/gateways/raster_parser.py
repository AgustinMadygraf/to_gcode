from typing import List, Set, Tuple
from src.dominio.entidades.geometria import Trayectoria as DomainTrayectoria, Punto
from src.application.boundaries.infrastructure_interfaces import SkeletonAbstraction, RasterImageProcessor
from src.application.boundaries.gateways import RasterParser as RasterParserBoundary

class RasterParser(RasterParserBoundary):
    def __init__(self, processor: RasterImageProcessor):
        self.processor = processor

    def parse_image(self, image_bytes: bytes) -> List[DomainTrayectoria]:
        skeleton = self.processor.process_image_to_skeleton(image_bytes)
        return self._trace_skeleton(skeleton)

    def _trace_skeleton(self, skeleton: SkeletonAbstraction) -> List[DomainTrayectoria]:
        paths: List[DomainTrayectoria] = []
        visited: Set[Tuple[int, int]] = set()
        rows, cols = skeleton.rows, skeleton.cols

        for r in range(rows):
            for c in range(cols):
                if skeleton.is_set(r, c) and (r, c) not in visited:
                    path_points: List[Tuple[int, int]] = []
                    # Use iterative approach to avoid RecursionError
                    stack = [(r, c)]
                    while stack:
                        curr_r, curr_c = stack.pop()
                        if (curr_r, curr_c) in visited:
                            continue
                            
                        visited.add((curr_r, curr_c))
                        path_points.append((curr_r, curr_c))
                        
                        for dr in [-1, 0, 1]:
                            for dc in [-1, 0, 1]:
                                if dr == 0 and dc == 0:
                                    continue
                                nr, nc = curr_r + dr, curr_c + dc
                                if 0 <= nr < rows and 0 <= nc < cols:
                                    if skeleton.is_set(nr, nc) and (nr, nc) not in visited:
                                        stack.append((nr, nc))
                                        
                    if len(path_points) > 1:
                        paths.append(DomainTrayectoria(points=[Punto(x=float(c), y=float(rows - r)) for r, c in path_points]))
        return paths
