"""
Path: src/aplicacion/casos_de_uso/convertir_imagen.py
"""

from typing import List
from src.aplicacion.casos_de_uso.convertidor_base import ConvertidorBaseGCode
from src.aplicacion.limites.puertos import AnalizadorRaster, GeneradorGCode
from src.aplicacion.limites.interfaz_repositorio_configuracion_maquina import RepositorioConfiguracionMaquina
from src.dominio.interfaces.optimizador_trayectoria import OptimizadorTrayectoria
from src.aplicacion.servicios.servicio_preparacion_trayectoria import ServicioPreparacionTrayectoria
from src.dominio.entidades.geometria import Trayectoria

class ConvertirImagenAGCode(ConvertidorBaseGCode):
    def __init__(
        self, 
        parser: AnalizadorRaster, 
        generator: GeneradorGCode, 
        repo: RepositorioConfiguracionMaquina,
        preparation_service: ServicioPreparacionTrayectoria,
        optimizer: OptimizadorTrayectoria
    ):
        super().__init__(generator, repo, preparation_service, optimizer)
        self.parser = parser

    def _parsear_entrada(self, input_data: bytes) -> List[Trayectoria]:
        return self.parser.parsear_imagen(input_data)
