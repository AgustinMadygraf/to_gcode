"""
Path: src/domain/services/geometry_service.py
"""

from typing import Any, Dict, List, Optional
from src.domain.interfaces.geometry_processor import GeometryProcessor
from src.domain.entities.machine_config import Point

class GeometryService:
    def __init__(self, geometry_processor: GeometryProcessor):
        self.processor = geometry_processor

    def transform_paths(self, raw_paths: List[Any], config: Any) -> List[Any]:
        # Existing logic...
        return raw_paths

    def fit_arc(self, points: List[Point], tolerance: float) -> Optional[Dict[str, Any]]:
        if len(points) < 3:
            return None
            
        p1, p2, p3 = points[0], points[len(points)//2], points[-1]
        circle = self.processor.get_circle_from_three_points(p1, p2, p3)
        if not circle:
            return None
            
        center, radius = circle
        max_dev, max_idx = self.processor.calculate_max_deviation(points, center, radius)
        
        if max_dev <= tolerance:
            return {"center": center, "radius": radius, "points": points}
        
        # Recursive split
        split_idx = max_idx
        left_arc = self.fit_arc(points[:split_idx+1], tolerance)
        right_arc = self.fit_arc(points[split_idx:], tolerance)
        
        return {"left": left_arc, "right": right_arc}
