"""
Path: src/application/boundaries/gateways.py
"""

from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.machine_config import Path, MachineConfig

class VectorParser(ABC):
    @abstractmethod
    def parse_svg(self, svg_content: str) -> List[Path]:
        pass

class GCodeGenerator(ABC):
    @abstractmethod
    def generate(self, paths: List[Path], config: MachineConfig) -> str:
        pass

class RasterParser(ABC):
    @abstractmethod
    def parse_image(self, image_bytes: bytes) -> List[Path]:
        pass
