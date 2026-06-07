"""
Path: src/aplicacion/limites/puertos_casos_de_uso.py
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from src.aplicacion.dto.solicitudes import ConversionSvgRequest

class PuertoConversionSVG(ABC):
    @abstractmethod
    def ejecutar(self, datos_entrada: ConversionSvgRequest) -> str:
        pass

class PuertoConversionImagen(ABC):
    @abstractmethod
    def ejecutar(self, bytes_imagen: bytes) -> str:
        pass

class PuertoGestionConfiguracion(ABC):
    @abstractmethod
    def guardar(self, config_datos: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def obtener(self) -> Any:
        pass
