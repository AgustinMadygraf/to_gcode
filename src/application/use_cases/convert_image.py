"""
Path: src/application/use_cases/convert_image.py
"""

from src.application.boundaries.gateways import GCodeGenerator, RasterParser
from src.application.boundaries.machine_config_repository import MachineConfigRepository
from src.domain.services.geometry_service import GeometryService
from src.domain.services.path_optimizer import PathOptimizerService
from src.domain.interfaces.geometry_transformer import GeometryTransformerInterface
from src.domain.entities.geometry import Rect

class ConvertImageToGCode:
    def __init__(
        self, 
        parser: RasterParser, 
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
        self.transformer = transformer

    def execute(self, image_bytes: bytes) -> str:
        config = self.repo.get_config()
        if not config:
            raise ValueError("Machine configuration not found")

        raw_paths = self.parser.parse_image(image_bytes)

        # Dynamic limits based on machine configuration
        landscape_limits = Rect(0.0, 0.0, config.max_x, config.max_y)
        portrait_limits = Rect(0.0, 0.0, config.max_y, config.max_x)
        
        transformed_paths, _ = self.transformer.fit_and_orient(
            raw_paths, landscape_limits, portrait_limits
        )
        
        transformed_paths = self.optimizer.optimize(transformed_paths)
        return self.generator.generate(transformed_paths, config)
