"""
Path: src/infrastructure/numpy/skeleton_wrapper.py
"""

import numpy as np
from src.application.boundaries.infrastructure_interfaces import SkeletonAbstraction

class NumpySkeletonWrapper(SkeletonAbstraction):
    def __init__(self, skeleton: np.ndarray):
        self._skeleton = skeleton

    def is_set(self, r: int, c: int) -> bool:
        return bool(self._skeleton[r, c])

    @property
    def rows(self) -> int:
        return self._skeleton.shape[0]

    @property
    def cols(self) -> int:
        return self._skeleton.shape[1]
