from typing import List
from src.application.use_cases.base_converter import BaseGCodeConverter
from src.application.boundaries.gateways import RasterParser, GCodeGenerator
from src.application.boundaries.machine_config_repository import MachineConfigRepository
from src.domain.interfaces.path_optimizer import PathOptimizer
from src.application.services.path_preparation_service import PathPreparationService
from src.domain.entities.geometry import Path

class ConvertImageToGCode(BaseGCodeConverter):
    def __init__(
        self, 
        parser: RasterParser, 
        generator: GCodeGenerator, 
        repo: MachineConfigRepository,
        preparation_service: PathPreparationService,
        optimizer: PathOptimizer
    ):
        super().__init__(generator, repo, preparation_service, optimizer)
        self.parser = parser

    def _parse_input(self, image_bytes: bytes) -> List[Path]:
        return self.parser.parse_image(image_bytes)
