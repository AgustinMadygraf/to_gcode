from abc import ABC, abstractmethod
from typing import Any, List
from src.application.boundaries.gateways import GCodeGenerator
from src.application.boundaries.machine_config_repository import MachineConfigRepository
from src.domain.interfaces.path_optimizer import PathOptimizer
from src.application.services.path_preparation_service import PathPreparationService
from src.domain.entities.geometry import Path

class BaseGCodeConverter(ABC):
    """
    Clase base que implementa el Template Method para la conversión a G-Code.
    Centraliza la orquestación común para todos los formatos de entrada.
    """
    def __init__(
        self,
        generator: GCodeGenerator,
        repo: MachineConfigRepository,
        preparation_service: PathPreparationService,
        optimizer: PathOptimizer
    ):
        self.generator = generator
        self.repo = repo
        self.preparation_service = preparation_service
        self.optimizer = optimizer

    @abstractmethod
    def _parse_input(self, input_data: Any) -> List[Path]:
        """Método abstracto para que cada formato implemente su propio parseo."""
        pass

    def execute(self, input_data: Any) -> str:
        """
        Orquestación estándar de la capa de aplicación.
        Sigue el flujo: Config -> Parse -> Prepare -> Optimize -> Generate.
        """
        config = self.repo.get_config()
        if not config:
            raise ValueError("Machine configuration not found")

        # 1. Parsear el input específico
        raw_paths = self._parse_input(input_data)

        # 2. Preparar (Escalado, Orientación, Marcas)
        transformed_paths = self.preparation_service.prepare(raw_paths, config)
        
        # 3. Optimizar (Minimizar movimientos en vacío)
        optimized_paths = self.optimizer.optimize(transformed_paths)
        
        # 4. Generar G-Code final
        return self.generator.generate(optimized_paths, config)
