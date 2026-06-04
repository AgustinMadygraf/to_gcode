"""
Path: src/adapters/gateways/gcode_generator.py
"""

from typing import List
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
        for path in paths:
            if not path.points:
                continue
            first = path.points[0]
            gcode_lines.append(config.pen_up_command)
            gcode_lines.append(self.wrapper.format_line("G0", {"X": first.x, "Y": first.y}))
            gcode_lines.append(config.pen_down_command)
            for p in path.points[1:]:
                gcode_lines.append(self.wrapper.format_line("G1", {"X": p.x, "Y": p.y}))
            
            gcode_lines.append(config.pen_up_command)

        gcode_lines.append(self.wrapper.format_line("G0", {"X": 0, "Y": 0}) + " " + self.wrapper.get_comment("Return home"))
        return '\n'.join(gcode_lines)
