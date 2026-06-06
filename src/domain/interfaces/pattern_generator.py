"""
Path: src/domain/interfaces/pattern_generator.py
"""

from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.geometry import Path

class TestPatternGeneratorInterface(ABC):
    @abstractmethod
    def generate(self, width: float, height: float, inset: float) -> List[Path]:
        pass
