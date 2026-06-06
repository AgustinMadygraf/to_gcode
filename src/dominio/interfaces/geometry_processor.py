"""
Path: src/domain/interfaces/geometry_processor.py
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from src.dominio.entidades.geometria import Punto

class GeometryProcessor(ABC):
    """Interfaz para procesamiento geométrico avanzado."""
    
    @abstractmethod
    def get_circle_from_three_points(self, p1: Punto, p2: Punto, p3: Punto) -> Optional[Tuple[Punto, float]]:
        """Calcula el centro y radio de un círculo que pasa por tres puntos."""
        pass
    
    @abstractmethod
    def calculate_max_deviation(self, points: List[Punto], center: Punto, radius: float) -> Tuple[float, int]:
        """Calcula la desviación máxima de un conjunto de puntos respecto a un arco."""
        pass
