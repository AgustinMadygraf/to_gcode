from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class PuertoConversionSVG(ABC):
    @abstractmethod
    def ejecutar(self, svg_content: str) -> str:
        pass

class PuertoConversionImagen(ABC):
    @abstractmethod
    def ejecutar(self, image_bytes: bytes) -> str:
        pass

class PuertoGestionConfiguracion(ABC):
    @abstractmethod
    def guardar(self, config_data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def obtener(self) -> Any:
        pass
