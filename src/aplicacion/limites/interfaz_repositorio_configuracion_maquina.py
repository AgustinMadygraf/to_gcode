"""
Path: src/aplicacion/limites/interfaz_repositorio_configuracion_maquina.py
"""

from abc import ABC, abstractmethod
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina

class RepositorioConfiguracionMaquina(ABC):
    @abstractmethod
    def obtener_configuracion(self) -> ConfiguracionMaquina | None:
        pass

    @abstractmethod
    def guardar_configuracion(self, config: ConfiguracionMaquina) -> None:
        pass
