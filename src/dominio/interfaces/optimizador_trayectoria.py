"""
Path: src/dominio/interfaces/optimizador_trayectoria.py
"""

from abc import ABC, abstractmethod
from typing import List
from src.dominio.entidades.geometria import Trayectoria

class OptimizadorTrayectoria(ABC):
    """Interfaz para estrategias de optimización de trayectorias."""
    
    @abstractmethod
    def optimizar(self, trayectorias: List[Trayectoria]) -> List[Trayectoria]:
        """Ordena y optimiza las trayectorias para minimizar movimientos en vacío."""
        pass
