"""
Trayectoria: src/infrastructure/math/diamond_pattern_generator.py
"""

from typing import List
from src.dominio.entidades.geometria import Trayectoria, Punto
from src.dominio.interfaces.generador_patrones import GeneradorPatrones

__all__ = ["DiamondPatternGenerator"]

class DiamondPatternGenerator(GeneradorPatrones):
    def generar(self, ancho: float, altura: float, margen: float) -> List[Trayectoria]:
        size = 10.0
        # Buffer to ensure diamond is fully within boundaries
        buffer = size / 2
        
        # Calculate safe corners
        # If corner is (margen, margen), points range from (margen-5, margen-5) to (margen+5, margen+5)
        # We need min coords to be >= 0 and max coords to be <= (ancho, altura)
        
        safe_x_min = margen + buffer
        safe_x_max = ancho - margen - buffer
        safe_y_min = margen + buffer
        safe_y_max = altura - margen - buffer
        
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
            paths.append(Trayectoria(puntos=points))
        return paths
