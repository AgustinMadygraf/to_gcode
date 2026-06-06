"""
Path: src/dominio/interfaces/generador_patrones.py
"""

from abc import ABC, abstractmethod
from typing import List
from src.dominio.entidades.geometria import Trayectoria

class GeneradorPatrones(ABC):
    @abstractmethod
    def generar(self, ancho: float, altura: float, margen: float) -> List[Trayectoria]:
        pass
