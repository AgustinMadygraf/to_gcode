"""
Path: src/domain/services/geometry_service.py
"""

from typing import List, Optional
from src.domain.interfaces.geometry_processor import GeometryProcessor
from src.domain.entities.geometry import Point, Arc, Path

class GeometryService:
    """Servicio de dominio para operaciones geométricas complejas."""
    
    def __init__(self, geometry_processor: GeometryProcessor):
        self.processor = geometry_processor

    def fit_arc(self, points: List[Point], tolerance: float) -> Optional[Arc]:
        """
        Intenta ajustar un arco circular a una secuencia de puntos.
        Retorna un objeto Arc si el ajuste está dentro de la tolerancia.
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
            return Arc(
                center=center,
                radius=radius,
                start_point=points[0],
                end_point=points[-1]
            )
        
        return None

    def simplify_path_to_arcs(self, path: Path, tolerance: float) -> List[Path]:
        """
        Divide una trayectoria en segmentos de líneas o arcos.
        (Lógica simplificada para ilustración del uso del nuevo VO Arc)
        """
        arc = self.fit_arc(path.points, tolerance)
        if arc:
            # Retornamos el mismo path pero enriquecido con info de arco
            return [Path(points=path.points, arc_info=arc)]
        return [path]
