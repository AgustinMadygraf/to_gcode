"""
Path: src/domain/interfaces/geometry_transformer.py
"""

from abc import ABC, abstractmethod
from typing import List, Tuple
from src.domain.entities.geometry import Path
from src.domain.entities.geometry import Rect

class GeometryTransformerInterface(ABC):
    @abstractmethod
    def fit_and_orient(self, paths: List[Path], landscape_limits: Rect, portrait_limits: Rect) -> Tuple[List[Path], str]:
        pass
