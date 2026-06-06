from src.aplicacion.limites.puertos_casos_de_uso import PuertoConversionImagen
from src.aplicacion.limites.puertos_casos_de_uso import PuertoConversionImagen
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

class ConvertirImagenAGCode(ConvertidorBaseGCode, PuertoConversionImagen):
    def __init__(
        self, 
        analizador: AnalizadorRaster, 
        generador: GeneradorGCode, 
        repositorio: RepositorioConfiguracionMaquina,
        servicio_preparacion: ServicioPreparacionTrayectoria,
        optimizador: OptimizadorTrayectoria
    ):
        super().__init__(generador=generador, repositorio=repositorio, servicio_preparacion=servicio_preparacion, optimizador=optimizador)
        self.analizador = analizador

    def _parsear_entrada(self, input_datos: bytes) -> List[Trayectoria]:
        return self.analizador.parsear_imagen(input_datos)
