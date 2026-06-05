"""
Path: src/application/boundaries/infrastructure_interfaces.py
"""

from abc import ABC, abstractmethod
from typing import List, Any, Dict, Optional, Generator

class SvgLibraryWrapper(ABC):
    @abstractmethod
    def get_paths_from_str(self, svg_content: str) -> List[Any]:
        pass

    @abstractmethod
    def sample_path(self, path: Any, num_samples: int) -> List[complex]:
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

class SkeletonAbstraction(ABC):
    @abstractmethod
    def is_set(self, r: int, c: int) -> bool:
        pass

    @property
    @abstractmethod
    def rows(self) -> int:
        pass

    @property
    @abstractmethod
    def cols(self) -> int:
        pass

class DatabaseSessionProvider(ABC):
    @abstractmethod
    def get_session(self) -> Generator[Any, None, None]:
        pass

from typing import Protocol, Tuple, Any

class ImageLike(Protocol):
    @property
    def shape(self) -> Tuple[int, ...]:
        ...
    def __getitem__(self, key: Any) -> Any:
        ...

class RasterImageProcessor(ABC):
    @abstractmethod
    def process_image_to_skeleton(self, image_bytes: bytes) -> SkeletonAbstraction:
        pass
