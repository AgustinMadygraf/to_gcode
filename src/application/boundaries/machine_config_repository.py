"""
Trayectoria: src/application/boundaries/machine_config_repository.py
"""

from abc import ABC, abstractmethod
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina

class ConfiguracionMaquinaRepository(ABC):
    @abstractmethod
    def get_config(self) -> ConfiguracionMaquina | None:
        pass

    @abstractmethod
    def save_config(self, config: ConfiguracionMaquina) -> None:
        pass
