"""
Path: src/application/boundaries/gateways.py
"""

from abc import ABC, abstractmethod
from src.domain.entities.machine_config import Path, MachineConfig

class VectorParser(ABC):
    @abstractmethod
    def parse_svg(self, svg_content: str) -> list[Path]:
        pass

class GCodeGenerator(ABC):    
    @abstractmethod
    def generate(self, paths: list[Path], config: MachineConfig) -> str:
        pass
