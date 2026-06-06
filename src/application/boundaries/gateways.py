"""
Trayectoria: src/application/boundaries/gateways.py
"""

from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.geometria import Trayectoria
from src.domain.entities.configuracion_maquina import ConfiguracionMaquina

class VectorParser(ABC):
    @abstractmethod
    def parse_svg(self, svg_content: str) -> List[Trayectoria]:
        pass

class GCodeGenerator(ABC):
    @abstractmethod
    def generate(self, paths: List[Trayectoria], config: ConfiguracionMaquina) -> str:
        pass

class RasterParser(ABC):
    @abstractmethod
    def parse_image(self, image_bytes: bytes) -> List[Trayectoria]:
        pass
