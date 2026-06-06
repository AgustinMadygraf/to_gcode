"""
Path: src/dominio/interfaces/procesador_geometria.py
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from src.dominio.entidades.geometria import Punto

class ProcesadorGeometria(ABC):
    """Interfaz para procesamiento geométrico avanzado."""
    
    @abstractmethod
    def obtener_circulo_desde_tres_puntos(self, p1: Punto, p2: Punto, p3: Punto) -> Optional[Tuple[Punto, float]]:
        """Calcula el centro y radio de un círculo que pasa por tres puntos."""
        pass
    
    @abstractmethod
    def calcular_maxima_desviacion(self, puntos: List[Punto], centro: Punto, radio: float) -> Tuple[float, int]:
        """Calcula la desviación máxima de un conjunto de puntos respecto a un arco."""
        pass
