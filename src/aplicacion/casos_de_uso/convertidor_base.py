"""
Path: src/aplicacion/casos_de_uso/convertidor_base.py
"""

from abc import ABC, abstractmethod
from typing import Any, List, Optional
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina
from src.aplicacion.limites.puertos import GeneradorGCode
from src.aplicacion.limites.interfaz_repositorio_configuracion_maquina import RepositorioConfiguracionMaquina
from src.dominio.interfaces.optimizador_trayectoria import OptimizadorTrayectoria
from src.aplicacion.servicios.servicio_preparacion_trayectoria import ServicioPreparacionTrayectoria
from src.dominio.entidades.geometria import Trayectoria

class ConvertidorBaseGCode(ABC):
    """
    Clase base que implementa el Template Method para la conversión a G-Code.
    Centraliza la orquestación común para todos los formatos de entrada.
    """
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
        """Método abstracto para que cada formato implemente su propio parseo."""
        pass

    def ejecutar(self, datos_entrada: Any) -> str:
        """
        Orquestación estándar de la capa de aplicación.
        Sigue el flujo: Config -> Parse -> Prepare -> Optimize -> Generate.
        """
        config: Optional[ConfiguracionMaquina] = self.repositorio.obtener_configuracion()
        if not config:
            raise ValueError("Configuración de la máquina no encontrada")

        # 1. Parsear el input específico
        trayectorias_brutas = self._parsear_entrada(datos_entrada)

        # 2. Preparar (Escalado, Orientación, Marcas)
        trayectorias_transformadas = self.servicio_preparacion.preparar(trayectorias_brutas, config)
        
        # 3. Optimizar (Minimizar movimientos en vacío)
        trayectorias_optimizadas = self.optimizador.optimizar(trayectorias_transformadas)
        
        # 4. Generar G-Code final
        return self.generador.generar(trayectorias_optimizadas, config)
