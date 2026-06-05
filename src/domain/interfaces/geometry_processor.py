"""
Path: src/domain/interfaces/geometry_processor.py
"""

from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple

class GeometryProcessor(ABC):
    @abstractmethod
    def get_circle_from_three_points(self, p1: Any, p2: Any, p3: Any) -> Optional[Tuple[Any, float]]:
        pass
    
    @abstractmethod
    def calculate_max_deviation(self, points: List[Any], center: Any, radius: float) -> Tuple[float, int]:
        pass
