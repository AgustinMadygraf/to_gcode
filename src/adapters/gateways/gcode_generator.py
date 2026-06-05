"""
Path: src/adapters/gateways/gcode_generator.py
"""

from typing import List
from src.application.boundaries.gateways import GCodeGenerator
from src.application.boundaries.infrastructure_interfaces import GCodeLibraryWrapper
from src.domain.entities.machine_config import Path, MachineConfig
from src.domain.services.geometry_service import GeometryService

class PyGCodeGenerator(GCodeGenerator):
    def __init__(self, wrapper: GCodeLibraryWrapper, geometry_service: GeometryService):
        self.wrapper = wrapper
        self.geometry_service = geometry_service

    def generate(self, paths: List[Path], config: MachineConfig) -> str:
        gcode_lines: List[str] = [
            self.wrapper.format_line("G21") + " " + self.wrapper.get_comment("Units in mm"),
            self.wrapper.format_line("G90") + " " + self.wrapper.get_comment("Absolute coordinates"),
            self.wrapper.format_line("G0", {"F": config.feedrate_move}),
            self.wrapper.format_line("G1", {"F": config.feedrate_draw})
        ]
        
        TOLERANCE = 0.5

        for path in paths:
            if not path.points:
                continue
            
            gcode_lines.append(config.pen_up_command)
            gcode_lines.append(self.wrapper.format_line("G0", {"X": path.points[0].x, "Y": path.points[0].y}))
            gcode_lines.append(config.pen_down_command)
            
            # Simple Arc Fitting attempt
            arc_fit = self.geometry_service.fit_arc(path.points, TOLERANCE)
            
            if arc_fit and "center" in arc_fit:
                # Direct Arc
                end_point = arc_fit["points"][-1]
                gcode_lines.append(self.wrapper.format_line("G2", {"X": end_point.x, "Y": end_point.y, "I": arc_fit["center"].x - path.points[0].x, "J": arc_fit["center"].y - path.points[0].y}))
            else:
                # Linear fallback
                for p in path.points[1:]:
                    gcode_lines.append(self.wrapper.format_line("G1", {"X": p.x, "Y": p.y}))
            
            gcode_lines.append(config.pen_up_command)

        gcode_lines.append(self.wrapper.format_line("G0", {"X": 0, "Y": 0}) + " " + self.wrapper.get_comment("Return home"))
        return '\n'.join(gcode_lines)
