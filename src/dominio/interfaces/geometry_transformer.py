"""
Trayectoria: src/domain/interfaces/geometry_transformer.py
"""

from abc import ABC, abstractmethod
from typing import List, Tuple
from src.dominio.entidades.geometria import Trayectoria
from src.dominio.entidades.geometria import Rectangulo

class GeometryTransformerInterface(ABC):
    @abstractmethod
    def fit_and_orient(self, paths: List[Trayectoria], landscape_limits: Rectangulo, portrait_limits: Rectangulo) -> Tuple[List[Trayectoria], str]:
        pass
