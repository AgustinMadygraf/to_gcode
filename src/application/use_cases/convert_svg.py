"""
Path: src/application/use_cases/convert_svg.py
"""

from src.application.boundaries.gateways import VectorParser, GCodeGenerator
from src.application.boundaries.machine_config_repository import MachineConfigRepository
from src.domain.services.geometry_service import GeometryService
from src.domain.services.path_optimizer import PathOptimizerService

class ConvertSVGToGCode:
    def __init__(
        self, 
        parser: VectorParser, 
        generator: GCodeGenerator, 
        repo: MachineConfigRepository,
        geometry_service: GeometryService
    ):
        self.parser = parser
        self.generator = generator
        self.repo = repo
        self.geometry_service = geometry_service
        self.optimizer = PathOptimizerService()

    def execute(self, svg_content: str) -> str:
        config = self.repo.get_config()
        if not config:
            raise ValueError("Machine configuration not found")

        raw_paths = self.parser.parse_svg(svg_content)

        transformed_paths = self.geometry_service.transform_paths(raw_paths, config)
        transformed_paths = self.optimizer.optimize(transformed_paths)
        return self.generator.generate(transformed_paths, config)
