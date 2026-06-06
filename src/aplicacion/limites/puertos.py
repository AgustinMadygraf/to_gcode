"""
Trayectoria: src/aplicacion.limites.puertos.py
"""

from abc import ABC, abstractmethod
from typing import List
from src.dominio.entidades.geometria import Trayectoria
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina

class AnalizadorVectorial(ABC):
    @abstractmethod
    def parsear_svg(self, contenido_svg: str) -> List[Trayectoria]:
        pass

class GeneradorGCode(ABC):
    @abstractmethod
    def generar(self, trayectorias: List[Trayectoria], config: ConfiguracionMaquina) -> str:
        pass

class AnalizadorRaster(ABC):
    @abstractmethod
    def parsear_imagen(self, bytes_imagen: bytes) -> List[Trayectoria]:
        pass
