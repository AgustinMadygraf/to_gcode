from dataclasses import dataclass
from typing import List, Optional, Union
from abc import ABC, abstractmethod
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
class Arc:
    """Representa un arco circular puro."""
    center: Point
    radius: float
    start_point: Point
    end_point: Point
    is_clockwise: bool = True

class Segment(ABC):
    """Interfaz para segmentos de trayectoria."""
    @property
    @abstractmethod
    def start(self) -> Point: pass
    
    @property
    @abstractmethod
    def end(self) -> Point: pass

@dataclass(frozen=True)
class LineSegment(Segment):
    """Segmento de línea recta."""
    p1: Point
    p2: Point
    
    @property
    def start(self) -> Point: return self.p1
    
    @property
    def end(self) -> Point: return self.p2

@dataclass(frozen=True)
class ArcSegment(Segment):
    """Segmento de arco circular."""
    arc: Arc
    
    @property
    def start(self) -> Point: return self.arc.start_point
    
    @property
    def end(self) -> Point: return self.arc.end_point

@dataclass(frozen=True)
class Path:
    """
    Representa una trayectoria compuesta por puntos y/o segmentos.
    Mantiene compatibilidad con la lista de puntos mientras evoluciona.
    """
    points: List[Point]
    segments: Optional[List[Segment]] = None
    arc_info: Optional[Arc] = None

    @property
    def is_empty(self) -> bool:
        return len(self.points) == 0

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

    @property
    def total_distance(self) -> float:
        if len(self.points) < 2:
            return 0.0
        dist = 0.0
        for i in range(len(self.points) - 1):
            dist += self.points[i].distance_to(self.points[i+1])
        return dist

    def reversed(self) -> 'Path':
        return Path(points=self.points[::-1], arc_info=self.arc_info)

@dataclass(frozen=True)
class Rect:
    min_x: float
    min_y: float
    max_x: float
    max_y: float

    @property
    def width(self) -> float: return self.max_x - self.min_x
    @property
    def height(self) -> float: return self.max_y - self.min_y
