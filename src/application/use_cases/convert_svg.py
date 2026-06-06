from typing import List
from src.application.use_cases.base_converter import BaseGCodeConverter
from src.application.boundaries.gateways import VectorParser, GCodeGenerator
from src.application.boundaries.machine_config_repository import ConfiguracionMaquinaRepository
from src.domain.interfaces.path_optimizer import TrayectoriaOptimizer
from src.application.services.path_preparation_service import TrayectoriaPreparationService
from src.domain.entities.geometria import Trayectoria

class ConvertSVGToGCode(BaseGCodeConverter):
    def __init__(
        self, 
        parser: VectorParser, 
        generator: GCodeGenerator, 
        repo: ConfiguracionMaquinaRepository,
        preparation_service: TrayectoriaPreparationService,
        optimizer: TrayectoriaOptimizer
    ):
        super().__init__(generator, repo, preparation_service, optimizer)
        self.parser = parser

    def _parse_input(self, svg_content: str) -> List[Trayectoria]:
        return self.parser.parse_svg(svg_content)
