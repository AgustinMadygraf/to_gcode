import numpy as np
from src.adaptadores.pasarelas.envoltorios_tecnicos import AbstraccionEsqueleto

class NumpySkeletonWrapper(AbstraccionEsqueleto):
    def __init__(self, skeleton: np.ndarray):
        self._skeleton = skeleton

    @property
    def ancho(self) -> int:
        return self._skeleton.shape[1]

    @property
    def alto(self) -> int:
        return self._skeleton.shape[0]

    @property
    def filas(self) -> int:
        return self.alto

    @property
    def columnas(self) -> int:
        return self.ancho

    def esta_pixel_encendido(self, x: int, y: int) -> bool:
        # Nota: La interfaz abstracta usaba (x, y), pero la implementación numpy usa (fila, col) -> (y, x)
        return bool(self._skeleton[y, x])
