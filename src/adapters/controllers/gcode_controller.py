"""
Path: src/adapters/controllers/gcode_controller.py
"""

from typing import Dict, Any, Optional
from src.application.use_cases.convert_svg import ConvertSVGToGCode
from src.application.use_cases.convert_image import ConvertImageToGCode
from src.application.boundaries.machine_config_repository import MachineConfigRepository
from src.domain.entities.machine_config import MachineConfig

class GCodeController:
    def __init__(
        self, 
        svg_converter: ConvertSVGToGCode, 
        image_converter: ConvertImageToGCode,
        repo: MachineConfigRepository
    ):
        self.svg_converter = svg_converter
        self.image_converter = image_converter
        self.repo = repo

    def set_config(self, config_data: Dict[str, Any]) -> Dict[str, str]:
        entity = MachineConfig(**config_data)
        self.repo.save_config(entity)
        return {"message": "Config saved"}

    def get_config(self) -> Optional[Dict[str, Any]]:
        config = self.repo.get_config()
        if not config:
            return None
        return {
            "name": config.name,
            "width": config.width,
            "height": config.height,
            "pen_up_command": config.pen_up_command,
            "pen_down_command": config.pen_down_command,
            "feedrate_draw": config.feedrate_draw,
            "feedrate_move": config.feedrate_move,
            "invert_y": config.invert_y,
            "scale_to_fit": config.scale_to_fit
        }

    def convert_svg(self, svg_content: str) -> Dict[str, str]:
        gcode = self.svg_converter.execute(svg_content)
        return {"gcode": gcode}

    def convert_image(self, image_bytes: bytes) -> Dict[str, str]:
        gcode = self.image_converter.execute(image_bytes)
        return {"gcode": gcode}
