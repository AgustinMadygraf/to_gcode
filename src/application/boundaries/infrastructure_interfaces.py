from abc import ABC, abstractmethod
from typing import List, Any, Dict, Optional, Generator, Protocol, runtime_checkable
from src.domain.entities.geometry import Point

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
    @abstractmethod
    def is_pixel_on(self, x: int, y: int) -> bool: ...

# --- Interfaces de Wrappers ---

class SvgLibraryWrapper(ABC):
    @abstractmethod
    def get_paths_from_str(self, svg_content: str) -> List[Any]:
        pass

    @abstractmethod
    def sample_path_to_domain(self, path: Any, num_samples: int) -> List[Point]:
        """Contrato mejorado: devuelve tipos de dominio, no tipos de librería."""
        pass

class RasterImageProcessor(ABC):
    @abstractmethod
    def process_image_to_skeleton(self, image_bytes: bytes) -> SkeletonAbstraction:
        pass

class GCodeLibraryWrapper(ABC):
    @abstractmethod
    def format_line(self, command: str, params: Optional[Dict[str, float]] = None) -> str:
        pass

    @abstractmethod
    def get_comment(self, text: str) -> str:
        pass

class ConfigPersistenceProvider(ABC):
    @abstractmethod
    def find_first(self) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def upsert(self, name: str, data: Dict[str, Any]) -> None:
        pass

class DatabaseSessionProvider(ABC):
    @abstractmethod
    def get_session(self) -> Generator[Any, None, None]:
        pass
