"""
Path: src/domain/interfaces/geometry_processor.py
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from src.domain.entities.geometry import Point

class GeometryProcessor(ABC):
    """Interfaz para procesamiento geométrico avanzado."""
    
    @abstractmethod
    def get_circle_from_three_points(self, p1: Point, p2: Point, p3: Point) -> Optional[Tuple[Point, float]]:
        """Calcula el centro y radio de un círculo que pasa por tres puntos."""
        pass
    
    @abstractmethod
    def calculate_max_deviation(self, points: List[Point], center: Point, radius: float) -> Tuple[float, int]:
        """Calcula la desviación máxima de un conjunto de puntos respecto a un arco."""
        pass
