from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.geometry import Path

class PathOptimizer(ABC):
    """Interfaz para estrategias de optimización de trayectorias."""
    
    @abstractmethod
    def optimize(self, paths: List[Path]) -> List[Path]:
        """Ordena y optimiza las trayectorias para minimizar movimientos en vacío."""
        pass
