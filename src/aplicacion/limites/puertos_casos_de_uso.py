from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class PuertoConversionSVG(ABC):
    @abstractmethod
    def ejecutar(self, contenido_svg: str) -> str:
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
