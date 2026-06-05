from typing import List
from src.application.use_cases.base_converter import BaseGCodeConverter
from src.application.boundaries.gateways import VectorParser, GCodeGenerator
from src.application.boundaries.machine_config_repository import MachineConfigRepository
from src.domain.interfaces.path_optimizer import PathOptimizer
from src.application.services.path_preparation_service import PathPreparationService
from src.domain.entities.geometry import Path

class ConvertSVGToGCode(BaseGCodeConverter):
    def __init__(
        self, 
        parser: VectorParser, 
        generator: GCodeGenerator, 
        repo: MachineConfigRepository,
        preparation_service: PathPreparationService,
        optimizer: PathOptimizer
    ):
        super().__init__(generator, repo, preparation_service, optimizer)
        self.parser = parser

    def _parse_input(self, svg_content: str) -> List[Path]:
        return self.parser.parse_svg(svg_content)
