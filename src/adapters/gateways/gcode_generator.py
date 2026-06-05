"""
Path: src/adapters/gateways/gcode_generator.py
"""

from typing import List, Optional
from src.application.boundaries.gateways import GCodeGenerator
from src.application.boundaries.infrastructure_interfaces import GCodeLibraryWrapper
from src.domain.entities.machine_config import Path, MachineConfig, Point
from src.domain.services.geometry_service import GeometryService

class PyGCodeGenerator(GCodeGenerator):
    def __init__(
        self, 
        wrapper: GCodeLibraryWrapper, 
        geometry_service: GeometryService,
        truncate_limit: Optional[int] = None,
        arc_tolerance: float = 2.0
    ):
        self.wrapper = wrapper
        self.geometry_service = geometry_service
        self.truncate_limit = truncate_limit
        self.arc_tolerance = arc_tolerance

    def _simplify_path(self, points: List[Point]) -> List[Point]:
        if len(points) < 3:
            return points
        
        simplified = [points[0]]
        for i in range(1, len(points) - 1):
            p1, p2, p3 = points[i-1], points[i], points[i+1]
            if abs((p2.y - p1.y) * (p3.x - p2.x) - (p2.x - p1.x) * (p3.y - p2.y)) > 1e-9:
                simplified.append(p2)
        simplified.append(points[-1])
        return simplified

    def generate(self, paths: List[Path], config: MachineConfig) -> str:
        gcode_lines: List[str] = [
            self.wrapper.format_line("G21") + " " + self.wrapper.get_comment("Units in mm"),
            self.wrapper.format_line("G90") + " " + self.wrapper.get_comment("Absolute coordinates"),
            self.wrapper.format_line("G0", {"F": config.feedrate_move}),
            self.wrapper.format_line("G1", {"F": config.feedrate_draw})
        ]
        
        for path in paths:
            if not path.points:
                continue
            
            # 1. Apply simplification
            simplified_points = self._simplify_path(path.points)
            
            gcode_lines.append(config.pen_up_command)
            gcode_lines.append(self.wrapper.format_line("G0", {"X": simplified_points[0].x, "Y": simplified_points[0].y}))
            gcode_lines.append(config.pen_down_command)
            
            # 2. Arc Fitting attempt on simplified points
            arc_fit = self.geometry_service.fit_arc(simplified_points, self.arc_tolerance)
            
            if arc_fit and "center" in arc_fit:
                # Direct Arc
                end_point = arc_fit["points"][-1]
                gcode_lines.append(self.wrapper.format_line("G2", {"X": end_point.x, "Y": end_point.y, "I": arc_fit["center"].x - simplified_points[0].x, "J": arc_fit["center"].y - simplified_points[0].y}))
            else:
                # Linear fallback using simplified points
                for p in simplified_points[1:]:
                    gcode_lines.append(self.wrapper.format_line("G1", {"X": p.x, "Y": p.y}))
            
            gcode_lines.append(config.pen_up_command)

        gcode_lines.append(self.wrapper.format_line("G0", {"X": 0, "Y": 0}) + " " + self.wrapper.get_comment("Return home"))
        
        # Truncate if configured
        if self.truncate_limit and self.truncate_limit > 0:
            return '\n'.join(gcode_lines[:self.truncate_limit])
            
        return '\n'.join(gcode_lines)
