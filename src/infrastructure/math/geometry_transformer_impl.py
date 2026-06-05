"""
Path: src/infrastructure/math/geometry_transformer_impl.py
"""

from typing import List, Tuple
import math
from src.domain.entities.geometry import Path, Point as DomainPoint
from src.domain.entities.geometry import Rect
from src.domain.interfaces.geometry_transformer import GeometryTransformerInterface

class GeometryTransformerImpl(GeometryTransformerInterface):
    def _get_bounding_box(self, paths: List[Path]) -> Rect:
        all_points = [p for path in paths for p in path.points]
        if not all_points:
            return Rect(0.0, 0.0, 0.0, 0.0)
        
        min_x = min(p.x for p in all_points)
        max_x = max(p.x for p in all_points)
        min_y = min(p.y for p in all_points)
        max_y = max(p.y for p in all_points)
        return Rect(min_x, min_y, max_x, max_y)

    def _rotate_path(self, path: Path, angle_deg: float) -> Path:
        angle_rad = math.radians(angle_deg)
        new_points: List[DomainPoint] = []
        for p in path.points:
            new_x = p.x * math.cos(angle_rad) - p.y * math.sin(angle_rad)
            new_y = p.x * math.sin(angle_rad) + p.y * math.cos(angle_rad)
            new_points.append(DomainPoint(x=new_x, y=new_y))
        
        min_x = min(p.x for p in new_points)
        min_y = min(p.y for p in new_points)
        normalized_points = [DomainPoint(x=p.x - min_x, y=p.y - min_y) for p in new_points]
        
        return Path(points=normalized_points)

    def _scale_and_translate(self, paths: List[Path], scale: float, offset: DomainPoint) -> List[Path]:
        transformed_paths: List[Path] = []
        for path in paths:
            new_points = [
                DomainPoint(x=p.x * scale + offset.x, y=p.y * scale + offset.y)
                for p in path.points
            ]
            transformed_paths.append(Path(points=new_points))
        return transformed_paths

    def fit_and_orient(self, paths: List[Path], landscape_limits: Rect, portrait_limits: Rect) -> Tuple[List[Path], str]:
        drawing_box = self._get_bounding_box(paths)
        
        scale_l = min(landscape_limits.width / drawing_box.width, landscape_limits.height / drawing_box.height)
        scale_p = min(portrait_limits.width / drawing_box.width, portrait_limits.height / drawing_box.height)
        
        if scale_p > scale_l:
            best_scale = scale_p
            orientation = "portrait"
            paths = [self._rotate_path(p, 90) for p in paths]
            final_drawing_box = self._get_bounding_box(paths)
            target_box = portrait_limits
        else:
            best_scale = scale_l
            orientation = "landscape"
            final_drawing_box = drawing_box
            target_box = landscape_limits
            
        offset = DomainPoint(x=target_box.min_x - final_drawing_box.min_x * best_scale, 
                             y=target_box.min_y - final_drawing_box.min_y * best_scale)
        
        transformed_paths = self._scale_and_translate(paths, best_scale, offset)
        
        return transformed_paths, orientation
