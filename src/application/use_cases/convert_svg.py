from src.application.boundaries.gateways import VectorParser, GCodeGenerator
from src.application.boundaries.machine_config_repository import MachineConfigRepository
from src.domain.services.geometry_service import GeometryService

class ConvertSVGToGCode:
    def __init__(
        self, 
        parser: VectorParser, 
        generator: GCodeGenerator, 
        repo: MachineConfigRepository,
        geometry_service: GeometryService = GeometryService()
    ):
        self.parser = parser
        self.generator = generator
        self.repo = repo
        self.geometry_service = geometry_service

    def execute(self, svg_content: str, test_mode: bool = False) -> str:
        config = self.repo.get_config()
        if not config:
            raise ValueError("Machine configuration not found")

        raw_paths = self.parser.parse_svg(svg_content)

        transformed_paths = self.geometry_service.transform_paths(raw_paths, config)
        gcode = self.generator.generate(transformed_paths, config)

        if test_mode:
            gcode = "\n".join(gcode.splitlines()[:100])

        return gcode
