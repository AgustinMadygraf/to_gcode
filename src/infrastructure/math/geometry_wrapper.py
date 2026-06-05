"""
Path: src/infrastructure/math/geometry_wrapper.py
"""

import math
from typing import Tuple, Optional, List
from src.domain.entities.machine_config import Point
from src.domain.interfaces.geometry_processor import GeometryProcessor

class GeometryWrapper(GeometryProcessor):
    def get_circle_from_three_points(self, p1: Point, p2: Point, p3: Point) -> Optional[Tuple[Point, float]]:
        """Calculates center and radius of a circle defined by three points."""
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y
        x3, y3 = p3.x, p3.y

        d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
        if abs(d) < 1e-9:  # Points are collinear
            return None

        ux = ((x1**2 + y1**2) * (y2 - y3) + (x2**2 + y2**2) * (y3 - y1) + (x3**2 + y3**2) * (y1 - y2)) / d
        uy = ((x1**2 + y1**2) * (x3 - x2) + (x2**2 + y2**2) * (x1 - x3) + (x3**2 + y3**2) * (x2 - x1)) / d
        
        center = Point(x=ux, y=uy)
        radius = math.sqrt((ux - x1)**2 + (uy - y1)**2)
        return center, radius

    def calculate_max_deviation(self, points: List[Point], center: Point, radius: float) -> Tuple[float, int]:
        """Calculates maximum deviation of points from a circle arc."""
        max_dev = 0.0
        max_idx = 0
        for i, p in enumerate(points):
            dist = math.sqrt((p.x - center.x)**2 + (p.y - center.y)**2)
            dev = abs(dist - radius)
            if dev > max_dev:
                max_dev = dev
                max_idx = i
        return max_dev, max_idx
