"""
Path: src/application/use_cases/convert_svg.py
"""

from src.application.boundaries.gateways import VectorParser, GCodeGenerator
from src.application.boundaries.machine_config_repository import MachineConfigRepository
from src.domain.services.geometry_service import GeometryService
from src.domain.services.path_optimizer import PathOptimizerService
from src.application.services.path_preparation_service import PathPreparationService
from src.domain.interfaces.geometry_transformer import GeometryTransformerInterface

class ConvertSVGToGCode:
    def __init__(
        self, 
        parser: VectorParser, 
        generator: GCodeGenerator, 
        repo: MachineConfigRepository,
        geometry_service: GeometryService,
        transformer: GeometryTransformerInterface
    ):
        self.parser = parser
        self.generator = generator
        self.repo = repo
        self.geometry_service = geometry_service
        self.optimizer = PathOptimizerService()
        self.preparation_service = PathPreparationService(transformer)

    def execute(self, svg_content: str) -> str:
        config = self.repo.get_config()
        if not config:
            raise ValueError("Machine configuration not found")

        raw_paths = self.parser.parse_svg(svg_content)
        
        # Use new preparation service
        transformed_paths = self.preparation_service.prepare(raw_paths, config)
        
        transformed_paths = self.optimizer.optimize(transformed_paths)
        return self.generator.generate(transformed_paths, config)
