"""
Path: src/adapters/gateways/gcode_generator.py
"""

from typing import Tuple, List
from src.application.boundaries.gateways import GCodeGenerator
from src.application.boundaries.infrastructure_interfaces import GCodeLibraryWrapper
from src.domain.entities.machine_config import Path, MachineConfig

class PyGCodeGenerator(GCodeGenerator):
    def __init__(self, wrapper: GCodeLibraryWrapper):
        self.wrapper = wrapper

    def generate(self, paths: List[Path], config: MachineConfig) -> str:
        gcode_lines: List[str] = [
            self.wrapper.format_line("G21") + " " + self.wrapper.get_comment("Units in mm"),
            self.wrapper.format_line("G90") + " " + self.wrapper.get_comment("Absolute coordinates"),
            self.wrapper.format_line("G0", {"F": config.feedrate_move}),
            self.wrapper.format_line("G1", {"F": config.feedrate_draw})
        ]

        scale: float = 1.0
        if config.scale_to_fit and paths:
            all_points = [p for path in paths for p in path.points]
            if all_points:
                min_x = min(p.x for p in all_points)
                max_x = max(p.x for p in all_points)
                min_y = min(p.y for p in all_points)
                max_y = max(p.y for p in all_points)
                svg_w = max_x - min_x
                svg_h = max_y - min_y
                if svg_w > 0 and svg_h > 0:
                    scale = min(config.width / svg_w, config.height / svg_h)

        for path in paths:
            if not path.points:
                continue
            first = path.points[0]
            fx, fy = self._transform(first.x, first.y, scale, config)
            gcode_lines.append(config.pen_up_command)
            gcode_lines.append(self.wrapper.format_line("G0", {"X": fx, "Y": fy}))
            gcode_lines.append(config.pen_down_command)
            for p in path.points[1:]:
                tx, ty = self._transform(p.x, p.y, scale, config)
                gcode_lines.append(self.wrapper.format_line("G1", {"X": tx, "Y": ty}))
            gcode_lines.append(config.pen_up_command)

        gcode_lines.append(self.wrapper.format_line("G0", {"X": 0, "Y": 0}) + " " + self.wrapper.get_comment("Return home"))
        return '\n'.join(gcode_lines)

    def _transform(self, x: float, y: float, scale: float, config: MachineConfig) -> Tuple[float, float]:
        tx: float = x * scale
        ty: float = y * scale
        if config.invert_y:
            ty = config.height - ty
        return tx, ty
