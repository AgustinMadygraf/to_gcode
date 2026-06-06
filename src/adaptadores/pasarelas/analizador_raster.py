"""
Path: src/adapters/pasarelas/raster_parser.py
"""

from typing import List, Set, Tuple
from src.dominio.entidades.geometria import Trayectoria as DomainTrayectoria, Punto
from src.adaptadores.pasarelas.envoltorios_tecnicos import SkeletonAbstraction, ProcesadorImagenRaster
from src.aplicacion.limites.puertos import AnalizadorRaster as AnalizadorRasterBoundary

class AnalizadorRaster(AnalizadorRasterBoundary):
    def __init__(self, processor: ProcesadorImagenRaster):
        self.processor = processor

    def parsear_imagen(self, bytes_imagen: bytes) -> List[DomainTrayectoria]:
        skeleton = self.processor.procesar_imagen_a_esqueleto(bytes_imagen)
        return self._trace_skeleton(skeleton)

    def _trace_skeleton(self, skeleton: SkeletonAbstraction) -> List[DomainTrayectoria]:
        paths: List[DomainTrayectoria] = []
        visited: Set[Tuple[int, int]] = set()
        rows, cols = skeleton.rows, skeleton.cols

        for r in range(rows):
            for c in range(cols):
                if skeleton.is_pixel_on(c, r) and (r, c) not in visited:
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
                                    if skeleton.is_pixel_on(nc, nr) and (nr, nc) not in visited:
                                        stack.append((nr, nc))
                                        
                    if len(path_points) > 1:
                        paths.append(DomainTrayectoria(puntos=[Punto(x=float(c), y=float(rows - r)) for r, c in path_points]))
        return paths
