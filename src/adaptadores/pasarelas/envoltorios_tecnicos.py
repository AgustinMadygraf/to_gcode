from abc import ABC, abstractmethod
from typing import List, Any, Dict, Optional, Generator, Protocol, runtime_checkable
from src.dominio.entidades.geometria import Punto

@runtime_checkable
class ImagenParecida(Protocol):
    @property
    def shape(self) -> tuple[int, ...]: ...
    def __getitem__(self, key: Any) -> Any: ...

class AbstraccionEsqueleto(ABC):
    @property
    @abstractmethod
    def ancho(self) -> int: ...

    @property
    @abstractmethod
    def alto(self) -> int: ...

    @property
    @abstractmethod
    def filas(self) -> int: ...

    @property
    @abstractmethod
    def columnas(self) -> int: ...
    
    @abstractmethod
    def esta_pixel_encendido(self, x: int, y: int) -> bool: ...

class EnvoltorioLibreriaSvg(ABC):
    @abstractmethod
    def obtener_trayectorias_desde_str(self, contenido_svg: str) -> List[Any]:
        pass

    @abstractmethod
    def muestrear_trayectoria_a_dominio(self, trayectoria: Any, num_muestras: int) -> List[Punto]:
        pass

class ProcesadorImagenRaster(ABC):
    @abstractmethod
    def procesar_imagen_a_esqueleto(self, bytes_imagen: bytes) -> AbstraccionEsqueleto:
        pass

class EnvoltorioLibreriaGCode(ABC):
    @abstractmethod
    def formatear_linea(self, comando: str, parametros: Optional[Dict[str, float]] = None) -> str:
        pass

    @abstractmethod
    def obtener_comentario(self, texto: str) -> str:
        pass

class ProveedorPersistenciaConfiguracion(ABC):
    @abstractmethod
    def buscar_primero(self) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def actualizar_o_insertar(self, nombre: str, datos: Dict[str, Any]) -> None:
        pass

class ProveedorSesionBaseDatos(ABC):
    @abstractmethod
    def obtener_sesion(self) -> Generator[Any, None, None]:
        pass
