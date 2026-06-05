from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Point:
    """Representa un punto en el plano 2D."""
    x: float
    y: float

@dataclass(frozen=True)
class Rect:
    """Representa un rectángulo delimitador (Bounding Box)."""
    min_x: float
    min_y: float
    max_x: float
    max_y: float

    @property
    def width(self) -> float:
        return self.max_x - self.min_x

    @property
    def height(self) -> float:
        return self.max_y - self.min_y

    @property
    def aspect_ratio(self) -> float:
        if self.height == 0:
            return 0.0
        return self.width / self.height

@dataclass(frozen=True)
class Path:
    """Representa una trayectoria compuesta por una secuencia de puntos."""
    points: List[Point]

    @property
    def is_empty(self) -> bool:
        return len(self.points) == 0

    @property
    def length(self) -> int:
        return len(self.points)
