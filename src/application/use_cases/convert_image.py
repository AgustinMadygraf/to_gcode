"""
Path: src/application/use_cases/convert_image.py
"""

from src.application.boundaries.gateways import GCodeGenerator, RasterParser
from src.application.boundaries.machine_config_repository import MachineConfigRepository
from src.domain.services.geometry_service import GeometryService

class ConvertImageToGCode:
    def __init__(
        self, 
        parser: RasterParser, 
        generator: GCodeGenerator, 
        repo: MachineConfigRepository,
        geometry_service: GeometryService
    ):
        self.parser = parser
        self.generator = generator
        self.repo = repo
        self.geometry_service = geometry_service

    def execute(self, image_bytes: bytes) -> str:
        config = self.repo.get_config()
        if not config:
            raise ValueError("Machine configuration not found")

        raw_paths = self.parser.parse_image(image_bytes)

        transformed_paths = self.geometry_service.transform_paths(raw_paths, config)
        return self.generator.generate(transformed_paths, config)
