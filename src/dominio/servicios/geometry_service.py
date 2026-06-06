"""
Trayectoria: src/domain/services/geometry_service.py
"""

from typing import List, Optional
from src.dominio.interfaces.geometry_processor import GeometryProcessor
from src.dominio.entidades.geometria import Punto, Arco, Trayectoria

class GeometryService:
    """Servicio de dominio para operaciones geométricas complejas."""
    
    def __init__(self, geometry_processor: GeometryProcessor):
        self.processor = geometry_processor

    def fit_arc(self, points: List[Punto], tolerance: float) -> Optional[Arco]:
        """
        Intenta ajustar un arco circular a una secuencia de puntos.
        Retorna un objeto Arco si el ajuste está dentro de la tolerancia.
        """
        if len(points) < 3:
            return None
            
        p1, p2, p3 = points[0], points[len(points)//2], points[-1]
        circle = self.processor.get_circle_from_three_points(p1, p2, p3)
        if not circle:
            return None
            
        center, radius = circle
        max_dev, _ = self.processor.calculate_max_deviation(points, center, radius)
        
        if max_dev <= tolerance:
            return Arco(
                center=center,
                radius=radius,
                start_point=points[0],
                end_point=points[-1]
            )
        
        return None

    def simplify_path_to_arcs(self, path: Trayectoria, tolerance: float) -> List[Trayectoria]:
        """
        Divide una trayectoria en segmentos de líneas o arcos.
        (Lógica simplificada para ilustración del uso del nuevo VO Arco)
        """
        arc = self.fit_arc(path.points, tolerance)
        if arc:
            # Retornamos el mismo path pero enriquecido con info de arco
            return [Trayectoria(points=path.points, arc_info=arc)]
        return [path]
