"""
Path: src/domain/entities/geometry.py
"""

from dataclasses import dataclass
from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float

@dataclass(frozen=True)
class Rect:
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
        if self.height == 0: return 0.0
        return self.width / self.height
