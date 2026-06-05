import numpy as np
from src.application.boundaries.infrastructure_interfaces import SkeletonAbstraction

class NumpySkeletonWrapper(SkeletonAbstraction):
    def __init__(self, skeleton: np.ndarray):
        self._skeleton = skeleton

    @property
    def width(self) -> int:
        return self._skeleton.shape[1]

    @property
    def height(self) -> int:
        return self._skeleton.shape[0]

    # Compatibilidad con implementación original
    @property
    def rows(self) -> int:
        return self.height

    @property
    def cols(self) -> int:
        return self.width

    def is_pixel_on(self, x: int, y: int) -> bool:
        # Nota: La interfaz abstracta usaba (x, y), pero la implementación numpy usa (fila, col) -> (y, x)
        return bool(self._skeleton[y, x])
