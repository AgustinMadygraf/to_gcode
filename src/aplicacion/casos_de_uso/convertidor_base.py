"""
Path: src/aplicacion/casos_de_uso/convertidor_base.py
"""

from abc import ABC, abstractmethod
from typing import Any, List
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
        generator: GeneradorGCode,
        repo: RepositorioConfiguracionMaquina,
        preparation_service: ServicioPreparacionTrayectoria,
        optimizer: OptimizadorTrayectoria
    ):
        self.generator = generator
        self.repo = repo
        self.preparation_service = preparation_service
        self.optimizer = optimizer

    @abstractmethod
    def _parsear_entrada(self, input_data: Any) -> List[Trayectoria]:
        """Método abstracto para que cada formato implemente su propio parseo."""
        pass

    def ejecutar(self, input_data: Any) -> str:
        """
        Orquestación estándar de la capa de aplicación.
        Sigue el flujo: Config -> Parse -> Prepare -> Optimize -> Generate.
        """
        config = self.repo.obtener_configuracion()
        if not config:
            raise ValueError("Configuración de la máquina no encontrada")

        # 1. Parsear el input específico
        raw_paths = self._parsear_entrada(input_data)

        # 2. Preparar (Escalado, Orientación, Marcas)
        transformed_paths = self.preparation_service.preparar(raw_paths, config)
        
        # 3. Optimizar (Minimizar movimientos en vacío)
        optimized_paths = self.optimizer.optimizar(transformed_paths)
        
        # 4. Generar G-Code final
        return self.generator.generar(optimized_paths, config)
