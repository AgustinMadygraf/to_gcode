"""
Path: src/application/boundaries/infrastructure_interfaces.py
"""

from abc import ABC, abstractmethod
from typing import List, Any, Dict, Optional

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
