"""
Path: src/application/boundaries/machine_config_repository.py
"""

from abc import ABC, abstractmethod
from src.domain.entities.machine_config import MachineConfig

class MachineConfigRepository(ABC):
    @abstractmethod
    def get_config(self) -> MachineConfig | None:
        pass

    @abstractmethod
    def save_config(self, config: MachineConfig) -> None:
        pass
