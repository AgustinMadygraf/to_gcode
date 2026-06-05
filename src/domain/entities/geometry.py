from dataclasses import dataclass
from typing import List
import math

@dataclass(frozen=True)
class Point:
    """Representa un punto en el plano 2D con comportamiento métrico."""
    x: float
    y: float

    def distance_to(self, other: 'Point') -> float:
        """Calcula la distancia euclidiana hacia otro punto."""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

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
    """Representa una trayectoria con comportamiento de dominio."""
    points: List[Point]

    @property
    def is_empty(self) -> bool:
        return len(self.points) == 0

    @property
    def length(self) -> int:
        """Número de puntos en la trayectoria."""
        return len(self.points)

    @property
    def total_distance(self) -> float:
        """Suma de las distancias entre puntos consecutivos."""
        if len(self.points) < 2:
            return 0.0
        dist = 0.0
        for i in range(len(self.points) - 1):
            dist += self.points[i].distance_to(self.points[i+1])
        return dist

    @property
    def start_point(self) -> Point:
        if self.is_empty:
            raise ValueError("Empty path has no start point")
        return self.points[0]

    @property
    def end_point(self) -> Point:
        if self.is_empty:
            raise ValueError("Empty path has no end point")
        return self.points[-1]

    def reversed(self) -> 'Path':
        """Retorna una nueva trayectoria con los puntos en orden inverso."""
        return Path(points=self.points[::-1])
