"""
Path: src/aplicacion/servicios/servicio_preparacion_trayectoria.py
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
        transformador: TransformadorGeometria,
        generador_patrones: GeneradorPatrones
    ):
        self.transformador = transformador
        self.generador_patrones = generador_patrones

    def preparar(self, trayectorias: List[Trayectoria], config: ConfiguracionMaquina) -> List[Trayectoria]:
        patrones = self.generador_patrones.generar(config.ancho_maximo_maquina, config.alto_maximo_maquina, margen=5.0)
        
        todas_las_trayectorias = patrones + trayectorias
        
        limites_paisaje = Rectangulo(0.0, 0.0, config.ancho_maximo_maquina, config.alto_maximo_maquina)
        limites_retrato = Rectangulo(0.0, 0.0, config.alto_maximo_maquina, config.ancho_maximo_maquina)
        
        trayectorias_transformadas, _ = self.transformador.ajustar_y_orientar(
            todas_las_trayectorias, limites_paisaje, limites_retrato
        )
        return trayectorias_transformadas
