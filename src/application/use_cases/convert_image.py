from typing import List
from src.application.use_cases.base_converter import BaseGCodeConverter
from src.application.boundaries.gateways import RasterParser, GCodeGenerator
from src.application.boundaries.machine_config_repository import ConfiguracionMaquinaRepository
from src.domain.interfaces.path_optimizer import TrayectoriaOptimizer
from src.application.services.path_preparation_service import TrayectoriaPreparationService
from src.domain.entities.geometria import Trayectoria

class ConvertImageToGCode(BaseGCodeConverter):
    def __init__(
        self, 
        parser: RasterParser, 
        generator: GCodeGenerator, 
        repo: ConfiguracionMaquinaRepository,
        preparation_service: TrayectoriaPreparationService,
        optimizer: TrayectoriaOptimizer
    ):
        super().__init__(generator, repo, preparation_service, optimizer)
        self.parser = parser

    def _parse_input(self, image_bytes: bytes) -> List[Trayectoria]:
        return self.parser.parse_image(image_bytes)
