from src.application.boundaries.gateways import GCodeGenerator, RasterParser
from src.application.boundaries.machine_config_repository import MachineConfigRepository
from src.domain.services.geometry_service import GeometryService
from src.domain.interfaces.path_optimizer import PathOptimizer
from src.application.services.path_preparation_service import PathPreparationService
from src.domain.interfaces.geometry_transformer import GeometryTransformerInterface
from src.domain.interfaces.pattern_generator import TestPatternGeneratorInterface

class ConvertImageToGCode:
    def __init__(
        self, 
        parser: RasterParser, 
        generator: GCodeGenerator, 
        repo: MachineConfigRepository,
        geometry_service: GeometryService,
        transformer: GeometryTransformerInterface,
        pattern_generator: TestPatternGeneratorInterface,
        optimizer: PathOptimizer
    ):
        self.parser = parser
        self.generator = generator
        self.repo = repo
        self.geometry_service = geometry_service
        self.optimizer = optimizer
        self.preparation_service = PathPreparationService(transformer, pattern_generator)

    def execute(self, image_bytes: bytes) -> str:
        config = self.repo.get_config()
        if not config:
            raise ValueError("Machine configuration not found")

        raw_paths = self.parser.parse_image(image_bytes)

        transformed_paths = self.preparation_service.prepare(raw_paths, config)

        transformed_paths = self.optimizer.optimize(transformed_paths)
        return self.generator.generate(transformed_paths, config)
