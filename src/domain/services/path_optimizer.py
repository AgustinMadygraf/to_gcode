from typing import List
from src.domain.entities.geometry import Path, Point
import math

class PathOptimizerService:
    @staticmethod
    def _distance(p1: Point, p2: Point) -> float:
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    @staticmethod
    def _path_length(path: Path) -> float:
        length = 0.0
        for i in range(len(path.points) - 1):
            length += math.sqrt(
                (path.points[i+1].x - path.points[i].x)**2 + 
                (path.points[i+1].y - path.points[i].y)**2
            )
        return length

    def optimize(self, paths: List[Path]) -> List[Path]:
        # Filter out empty paths before processing
        valid_paths = [p for p in paths if p.points]
        if not valid_paths:
            return []
        
        # Sort paths by length in descending order first
        sorted_paths = sorted(valid_paths, key=self._path_length, reverse=True)
        
        # Start from the longest path
        current_path = sorted_paths[0]
        unvisited = sorted_paths[1:]
        
        optimized = [current_path]
        
        while unvisited:
            # Find the path whose start point is closest to current_path end point
            last_point = current_path.points[-1]
            next_path = min(unvisited, key=lambda p: self._distance(last_point, p.points[0]))
            
            unvisited.remove(next_path)
            optimized.append(next_path)
            current_path = next_path
            
        return optimized
