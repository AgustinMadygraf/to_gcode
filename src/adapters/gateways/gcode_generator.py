from src.application.boundaries.gateways import GCodeGenerator
from src.domain.entities.machine_config import Path, MachineConfig

class PyGCodeGenerator(GCodeGenerator):
    def generate(self, paths: list[Path], config: MachineConfig) -> str:
        gcode_lines = [
            f'G21 ; Units in mm',
            f'G90 ; Absolute coordinates',
            f'G0 F{config.feedrate_move}',
            f'G1 F{config.feedrate_draw}'
        ]

        scale = 1.0
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
            if not path.points: continue
            first = path.points[0]
            fx, fy = self._transform(first.x, first.y, scale, config)
            gcode_lines.append(config.pen_up_command)
            gcode_lines.append(f'G0 X{fx:.3f} Y{fy:.3f}')
            gcode_lines.append(config.pen_down_command)
            for p in path.points[1:]:
                tx, ty = self._transform(p.x, p.y, scale, config)
                gcode_lines.append(f'G1 X{tx:.3f} Y{ty:.3f}')
            gcode_lines.append(config.pen_up_command)

        gcode_lines.append('G0 X0 Y0 ; Return home')
        return '\n'.join(gcode_lines)

    def _transform(self, x, y, scale, config):
        tx = x * scale
        ty = y * scale
        if config.invert_y:
            ty = config.height - ty
        return tx, ty
