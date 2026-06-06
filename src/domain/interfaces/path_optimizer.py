"""
Trayectoria: src/domain/interfaces/path_optimizer.py
"""

from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.geometria import Trayectoria

class TrayectoriaOptimizer(ABC):
    """Interfaz para estrategias de optimización de trayectorias."""
    
    @abstractmethod
    def optimize(self, paths: List[Trayectoria]) -> List[Trayectoria]:
        """Ordena y optimiza las trayectorias para minimizar movimientos en vacío."""
        pass
