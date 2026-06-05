"""
Path: src/domain/interfaces/pattern_generator.py
"""

from typing import List
from src.domain.entities.geometry import Path

class TestPatternGeneratorInterface:
    def generate(self, width: float, height: float, inset: float) -> List[Path]:
        raise NotImplementedError
