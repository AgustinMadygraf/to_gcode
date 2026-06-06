"""
Trayectoria: src/infrastructure/math/geometry_wrapper.py
"""

import math
from typing import Tuple, Optional, List
from src.dominio.entidades.geometria import Punto
from src.dominio.interfaces.procesador_geometria import ProcesadorGeometria

class EnvoltorioGeometria(ProcesadorGeometria):
    def obtener_circulo_desde_tres_puntos(self, p1: Punto, p2: Punto, p3: Punto) -> Optional[Tuple[Punto, float]]:
        """Calculates center and radius of a circle defined by three points."""
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y
        x3, y3 = p3.x, p3.y

        d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
        if abs(d) < 1e-9:  # Puntos are collinear
            return None

        ux = ((x1**2 + y1**2) * (y2 - y3) + (x2**2 + y2**2) * (y3 - y1) + (x3**2 + y3**2) * (y1 - y2)) / d
        uy = ((x1**2 + y1**2) * (x3 - x2) + (x2**2 + y2**2) * (x1 - x3) + (x3**2 + y3**2) * (x2 - x1)) / d
        
        center = Punto(x=ux, y=uy)
        radius = math.sqrt((ux - x1)**2 + (uy - y1)**2)
        return center, radius

    def calcular_maxima_desviacion(self, puntos: List[Punto], centro: Punto, radio: float) -> Tuple[float, int]:
        """Calcula la desviación máxima de una lista de puntos respecto a un arco de círculo."""
        max_dev = 0.0
        max_idx = 0
        for i, p in enumerate(puntos):
            dist = math.sqrt((p.x - centro.x)**2 + (p.y - centro.y)**2)
            dev = abs(dist - radio)
            if dev > max_dev:
                max_dev = dev
                max_idx = i
        return max_dev, max_idx
