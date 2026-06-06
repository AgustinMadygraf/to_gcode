"""
Path: src/dominio/interfaces/transformador_geometria.py
"""

from abc import ABC, abstractmethod
from typing import List, Tuple
from src.dominio.entidades.geometria import Trayectoria, Rectangulo

class TransformadorGeometria(ABC):
    @abstractmethod
    def ajustar_y_orientar(self, trayectorias: List[Trayectoria], limites_paisaje: Rectangulo, limites_retrato: Rectangulo) -> Tuple[List[Trayectoria], str]:
        pass
