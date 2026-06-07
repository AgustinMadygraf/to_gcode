"""
Path: src/aplicacion/servicios/servicio_preparacion_trayectoria.py
"""

from typing import List
from src.dominio.entidades.geometria import Trayectoria, Rectangulo
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina
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
        # 1. Definir los límites de la máquina
        limites_paisaje = Rectangulo(0.0, 0.0, config.ancho_maximo_maquina, config.alto_maximo_maquina)
        limites_retrato = Rectangulo(0.0, 0.0, config.alto_maximo_maquina, config.ancho_maximo_maquina)
        
        # 2. Escalar y orientar solo el dibujo
        trayectorias_transformadas, _ = self.transformador.ajustar_y_orientar(
            trayectorias, limites_paisaje, limites_retrato
        )
        
        # 3. Generar patrones en los límites de la máquina (ahora que el dibujo ya está escalado)
        patrones = self.generador_patrones.generar(config.ancho_maximo_maquina, config.alto_maximo_maquina, margen=5.0)
        
        # 4. Unir dibujo transformado + patrones
        return patrones + trayectorias_transformadas
