"""
Trayectoria: src/application/services/path_preparation_service.py
"""

from typing import List
from src.domain.entities.geometria import Trayectoria
from src.domain.entities.configuracion_maquina import ConfiguracionMaquina
from src.domain.entities.geometria import Rectangulo
from src.domain.interfaces.geometry_transformer import GeometryTransformerInterface
from src.domain.interfaces.pattern_generator import TestPatternGeneratorInterface

class TrayectoriaPreparationService:
    def __init__(
        self, 
        transformer: GeometryTransformerInterface,
        pattern_generator: TestPatternGeneratorInterface
    ):
        self.transformer = transformer
        self.pattern_generator = pattern_generator

    def prepare(self, paths: List[Trayectoria], config: ConfiguracionMaquina) -> List[Trayectoria]:
        patterns = self.pattern_generator.generate(config.max_x, config.max_y, inset=5.0)
        
        all_paths = patterns + paths
        
        landscape_limits = Rectangulo(0.0, 0.0, config.max_x, config.max_y)
        portrait_limits = Rectangulo(0.0, 0.0, config.max_y, config.max_x)
        
        transformed_paths, _ = self.transformer.fit_and_orient(
            all_paths, landscape_limits, portrait_limits
        )
        return transformed_paths
