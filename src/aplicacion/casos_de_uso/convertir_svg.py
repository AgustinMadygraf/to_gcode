from src.aplicacion.limites.puertos_casos_de_uso import PuertoConversionSVG
from src.aplicacion.limites.puertos_casos_de_uso import PuertoConversionSVG
"""
Path: src/aplicacion/casos_de_uso/convertir_svg.py
"""

from typing import List
from src.aplicacion.casos_de_uso.convertidor_base import ConvertidorBaseGCode
from src.aplicacion.limites.puertos import AnalizadorVectorial, GeneradorGCode
from src.aplicacion.limites.interfaz_repositorio_configuracion_maquina import RepositorioConfiguracionMaquina
from src.dominio.interfaces.optimizador_trayectoria import OptimizadorTrayectoria
from src.aplicacion.servicios.servicio_preparacion_trayectoria import ServicioPreparacionTrayectoria
from src.dominio.entidades.geometria import Trayectoria
from src.dominio.servicios.especificaciones_trayectoria import TrayectoriaNoVacia
from src.dominio.excepciones.base import ReglaDeNegocioVioladaError

class ConvertirSVGAGCode(ConvertidorBaseGCode, PuertoConversionSVG):
    def __init__(
        self, 
        analizador: AnalizadorVectorial, 
        generador: GeneradorGCode, 
        repositorio: RepositorioConfiguracionMaquina,
        servicio_preparacion: ServicioPreparacionTrayectoria,
        optimizador: OptimizadorTrayectoria
    ):
        super().__init__(generador=generador, repositorio=repositorio, servicio_preparacion=servicio_preparacion, optimizador=optimizador)
        self.analizador = analizador

    def _parsear_entrada(self, input_datos: str) -> List[Trayectoria]:
        trayectorias = self.analizador.parsear_svg(input_datos)
        
        # Validar usando especificaciones
        validador = TrayectoriaNoVacia()
        for t in trayectorias:
            if not validador.es_satisfecha_por(t):
                raise ReglaDeNegocioVioladaError("Se encontró una trayectoria vacía en el SVG")
                
        return trayectorias
