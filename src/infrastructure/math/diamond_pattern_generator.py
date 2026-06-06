"""
Trayectoria: src/infrastructure/math/diamond_pattern_generator.py
"""

from typing import List
from src.domain.entities.geometria import Trayectoria, Punto
from src.domain.interfaces.pattern_generator import TestPatternGeneratorInterface

__all__ = ["DiamondPatternGenerator"]

class DiamondPatternGenerator(TestPatternGeneratorInterface):
    def generate(self, width: float, height: float, inset: float) -> List[Trayectoria]:
        size = 10.0
        # Buffer to ensure diamond is fully within boundaries
        buffer = size / 2
        
        # Calculate safe corners
        # If corner is (inset, inset), points range from (inset-5, inset-5) to (inset+5, inset+5)
        # We need min coords to be >= 0 and max coords to be <= (width, height)
        
        safe_x_min = inset + buffer
        safe_x_max = width - inset - buffer
        safe_y_min = inset + buffer
        safe_y_max = height - inset - buffer
        
        corners = [
            (safe_x_min, safe_y_min),
            (safe_x_max, safe_y_min),
            (safe_x_min, safe_y_max),
            (safe_x_max, safe_y_max)
        ]
        
        paths: List[Trayectoria] = []
        for cx, cy in corners:
            # Puntos around (cx, cy)
            points = [
                Punto(cx, cy - size/2),
                Punto(cx + size/2, cy),
                Punto(cx, cy + size/2),
                Punto(cx - size/2, cy),
                Punto(cx, cy - size/2)
            ]
            paths.append(Trayectoria(points=points))
        return paths
