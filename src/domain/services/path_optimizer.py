from typing import List
from src.domain.entities.machine_config import Path, Point
import math

class PathOptimizerService:
    @staticmethod
    def _distance(p1: Point, p2: Point) -> float:
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def optimize(self, paths: List[Path]) -> List[Path]:
        # Filter out empty paths before processing
        valid_paths = [p for p in paths if p.points]
        if not valid_paths:
            return []
        
        # Start from the path closest to origin (0,0)
        unvisited = valid_paths[:]
        current_path = min(unvisited, key=lambda p: self._distance(Point(0, 0), p.points[0]))
        unvisited.remove(current_path)
        
        optimized = [current_path]
        
        while unvisited:
            # Find the path whose start point is closest to current_path end point
            last_point = current_path.points[-1]
            next_path = min(unvisited, key=lambda p: self._distance(last_point, p.points[0]))
            
            unvisited.remove(next_path)
            optimized.append(next_path)
            current_path = next_path
            
        return optimized
