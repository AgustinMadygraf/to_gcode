"""
Trayectoria: src/domain/interfaces/pattern_generator.py
"""

from abc import ABC, abstractmethod
from typing import List
from src.dominio.entidades.geometria import Trayectoria

class TestPatternGeneratorInterface(ABC):
    @abstractmethod
    def generate(self, width: float, height: float, inset: float) -> List[Trayectoria]:
        pass
