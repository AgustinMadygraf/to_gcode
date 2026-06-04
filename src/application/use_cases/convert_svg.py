"""
Path: src/application/use_cases/convert_svg.py
"""

from src.application.boundaries.gateways import VectorParser, GCodeGenerator
from src.application.boundaries.machine_config_repository import MachineConfigRepository

class ConvertSVGToGCode:
    "Caso de uso para convertir un archivo SVG a G-code."
    def __init__(
        self, 
        parser: VectorParser, 
        generator: GCodeGenerator,
        repository: MachineConfigRepository
    ):
        self.parser = parser
        self.generator = generator
        self.repository = repository

    def execute(self, svg_content: str) -> str:
        config = self.repository.get_config()
        if not config:
            raise ValueError('La configuración de la máquina no ha sido establecida.')

        paths = self.parser.parse_svg(svg_content)

        return self.generator.generate(paths, config)
