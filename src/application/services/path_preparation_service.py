"""
Path: src/application/services/path_preparation_service.py
"""

from typing import List
from src.domain.entities.machine_config import Path, MachineConfig
from src.domain.entities.geometry import Rect
from src.domain.interfaces.geometry_transformer import GeometryTransformerInterface

class PathPreparationService:
    def __init__(self, transformer: GeometryTransformerInterface):
        self.transformer = transformer

    def prepare(self, paths: List[Path], config: MachineConfig) -> List[Path]:
        landscape_limits = Rect(0.0, 0.0, config.max_x, config.max_y)
        portrait_limits = Rect(0.0, 0.0, config.max_y, config.max_x)
        
        transformed_paths, _ = self.transformer.fit_and_orient(
            paths, landscape_limits, portrait_limits
        )
        return transformed_paths
