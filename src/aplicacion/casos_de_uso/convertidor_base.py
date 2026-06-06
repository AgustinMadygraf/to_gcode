"""
Path: src/aplicacion/casos_de_uso/convertidor_base.py
"""

from abc import ABC, abstractmethod
from src.dominio.excepciones.base import ConfiguracionNoEncontradaError
from typing import Any, List, Optional
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina
from src.aplicacion.limites.puertos import GeneradorGCode
from src.aplicacion.limites.interfaz_repositorio_configuracion_maquina import RepositorioConfiguracionMaquina
from src.dominio.interfaces.optimizador_trayectoria import OptimizadorTrayectoria
from src.aplicacion.servicios.servicio_preparacion_trayectoria import ServicioPreparacionTrayectoria
from src.dominio.entidades.geometria import Trayectoria

class ConvertidorBaseGCode(ABC):
    def __init__(
        self,
        generador: GeneradorGCode,
        repositorio: RepositorioConfiguracionMaquina,
        servicio_preparacion: ServicioPreparacionTrayectoria,
        optimizador: OptimizadorTrayectoria
    ):
        self.generador = generador
        self.repositorio = repositorio
        self.servicio_preparacion = servicio_preparacion
        self.optimizador = optimizador

    @abstractmethod
    def _parsear_entrada(self, input_data: Any) -> List[Trayectoria]:
        pass

    def ejecutar(self, datos_entrada: Any) -> str:
        config: Optional[ConfiguracionMaquina] = self.repositorio.obtener_configuracion()
        if not config:
            raise ConfiguracionNoEncontradaError("Configuración de la máquina no encontrada")

        trayectorias_brutas = self._parsear_entrada(datos_entrada)

        trayectorias_transformadas = self.servicio_preparacion.preparar(trayectorias_brutas, config)

        trayectorias_optimizadas = self.optimizador.optimizar(trayectorias_transformadas)

        return self.generador.generar(trayectorias_optimizadas, config)
