from typing import List
from src.application.use_cases.base_converter import BaseGCodeConverter
from src.application.boundaries.gateways import VectorParser, GCodeGenerator
from src.application.boundaries.machine_config_repository import ConfiguracionMaquinaRepository
from src.dominio.interfaces.path_optimizer import TrayectoriaOptimizer
from src.application.services.servicio_preparacion_trayectoria import ServicioPreparacionTrayectoria
from src.dominio.entidades.geometria import Trayectoria

class ConvertSVGToGCode(BaseGCodeConverter):
    def __init__(
        self, 
        parser: VectorParser, 
        generator: GCodeGenerator, 
        repo: ConfiguracionMaquinaRepository,
        preparation_service: ServicioPreparacionTrayectoria,
        optimizer: TrayectoriaOptimizer
    ):
        super().__init__(generator, repo, preparation_service, optimizer)
        self.parser = parser

    def _parse_input(self, svg_content: str) -> List[Trayectoria]:
        return self.parser.parse_svg(svg_content)
