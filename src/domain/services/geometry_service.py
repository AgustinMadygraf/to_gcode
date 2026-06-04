"""
Path: src/domain/services/geometry_service.py
"""

from typing import List, Tuple
from src.domain.entities.machine_config import MachineConfig, Path, Point

class GeometryService:
    def transform_paths(self, paths: List[Path], config: MachineConfig) -> List[Path]:
        scale = self._calculate_scale(paths, config)
        transformed_paths: List[Path] = []
        
        for path in paths:
            new_points: List[Point] = []
            for p in path.points:
                tx, ty = self._transform_point(p.x, p.y, scale, config)
                new_points.append(Point(x=tx, y=ty))
            transformed_paths.append(Path(points=new_points))
            
        return transformed_paths

    def _calculate_scale(self, paths: List[Path], config: MachineConfig) -> float:
        if not config.scale_to_fit or not paths:
            return 1.0
            
        all_points = [p for path in paths for p in path.points]
        if not all_points:
            return 1.0
            
        min_x = min(p.x for p in all_points)
        max_x = max(p.x for p in all_points)
        min_y = min(p.y for p in all_points)
        max_y = max(p.y for p in all_points)
        
        svg_w = max_x - min_x
        svg_h = max_y - min_y
        
        if svg_w <= 0 or svg_h <= 0:
            return 1.0
            
        return min(config.width / svg_w, config.height / svg_h)

    def _transform_point(self, x: float, y: float, scale: float, config: MachineConfig) -> Tuple[float, float]:
        tx = x * scale
        ty = y * scale
        if config.invert_y:
            ty = config.height - ty
        return tx, ty
