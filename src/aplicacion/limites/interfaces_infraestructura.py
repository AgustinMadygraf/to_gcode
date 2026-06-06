"""
Path: src/aplicacion/limites/interfaces_infraestructura.py
"""

from abc import ABC, abstractmethod
from typing import List, Any, Dict, Optional, Generator, Protocol, runtime_checkable
from src.dominio.entidades.geometria import Punto

# --- Protocols para desacoplamiento técnico ---

@runtime_checkable
class ImageLike(Protocol):
    @property
    def shape(self) -> tuple[int, ...]: ...
    def __getitem__(self, key: Any) -> Any: ...

class SkeletonAbstraction(ABC):
    @property
    @abstractmethod
    def width(self) -> int: ...

    @property
    @abstractmethod
    def height(self) -> int: ...

    @property
    @abstractmethod
    def rows(self) -> int: ...

    @property
    @abstractmethod
    def cols(self) -> int: ...

    
    @abstractmethod
    def is_pixel_on(self, x: int, y: int) -> bool: ...

# --- Interfaces de Wrappers ---

class EnvoltorioLibreriaSvg(ABC):
    @abstractmethod
    def obtener_trayectorias_desde_str(self, svg_content: str) -> List[Any]:
        pass

    @abstractmethod
    def muestrear_trayectoria_a_dominio(self, path: Any, num_samples: int) -> List[Punto]:
        pass

class ProcesadorImagenRaster(ABC):
    @abstractmethod
    def procesar_imagen_a_esqueleto(self, image_bytes: bytes) -> SkeletonAbstraction:
        pass

class EnvoltorioLibreriaGCode(ABC):
    @abstractmethod
    def formatear_linea(self, command: str, params: Optional[Dict[str, float]] = None) -> str:
        pass

    @abstractmethod
    def obtener_comentario(self, text: str) -> str:
        pass

class ProveedorPersistenciaConfiguracion(ABC):
    @abstractmethod
    def buscar_primero(self) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def actualizar_o_insertar(self, name: str, data: Dict[str, Any]) -> None:
        pass

class ProveedorSesionBaseDatos(ABC):
    @abstractmethod
    def obtener_sesion(self) -> Generator[Any, None, None]:
        pass
