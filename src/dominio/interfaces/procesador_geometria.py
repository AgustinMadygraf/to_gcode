"""
Path: src/dominio/interfaces/procesador_geometria.py
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from src.dominio.entidades.geometria import Punto

class ProcesadorGeometria(ABC):
    @abstractmethod
    def obtener_circulo_desde_tres_puntos(self, p1: Punto, p2: Punto, p3: Punto) -> Optional[Tuple[Punto, float]]:
        pass
    
    @abstractmethod
    def calcular_maxima_desviacion(self, puntos: List[Punto], centro: Punto, radio: float) -> Tuple[float, int]:
        pass
