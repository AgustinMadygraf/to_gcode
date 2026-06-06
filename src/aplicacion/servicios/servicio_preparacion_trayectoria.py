"""
Trayectoria: src/aplicacion.servicios/path_preparation_service.py
"""

from typing import List
from src.dominio.entidades.geometria import Trayectoria
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina
from src.dominio.entidades.geometria import Rectangulo
from src.dominio.interfaces.transformador_geometria import TransformadorGeometria
from src.dominio.interfaces.generador_patrones import GeneradorPatrones

class ServicioPreparacionTrayectoria:
    def __init__(
        self, 
        transformer: TransformadorGeometria,
        pattern_generator: GeneradorPatrones
    ):
        self.transformador = transformer
        self.generador_patrones = pattern_generator

    def preparar(self, paths: List[Trayectoria], config: ConfiguracionMaquina) -> List[Trayectoria]:
        patterns = self.generador_patrones.generar(config.max_x, config.max_y, margen=5.0)
        
        all_paths = patterns + paths
        
        landscape_limits = Rectangulo(0.0, 0.0, config.max_x, config.max_y)
        portrait_limits = Rectangulo(0.0, 0.0, config.max_y, config.max_x)
        
        transformed_paths, _ = self.transformador.fit_and_orient(
            all_paths, landscape_limits, portrait_limits
        )
        return transformed_paths
