"""
Path: src/domain/entities/machine_config.py
"""

from dataclasses import dataclass
from enum import Enum
from typing import NewType, Optional

# Abstracción semántica de la herramienta
class ToolState(Enum):
    UP = "UP"
    DOWN = "DOWN"

@dataclass(frozen=True)
class ToolAction:
    """Representa una acción de la herramienta sin depender de strings G-Code."""
    state: ToolState
    command_override: Optional[str] = None # Solo para excepciones técnicas

Feedrate = NewType('Feedrate', float)

@dataclass(frozen=True)
class MachineConfig:
    """Configuración de la máquina plotter con validación de consistencia física."""
    name: str
    width: float   # Área de trabajo lógica
    height: float  # Área de trabajo lógica
    max_x: float   # Límite físico hardware
    max_y: float   # Límite físico hardware
    pen_up_command: str   # Se mantiene para infraestructura pero el dominio usará ToolState
    pen_down_command: str
    feedrate_draw: Feedrate
    feedrate_move: Feedrate
    invert_y: bool = True
    scale_to_fit: bool = True

    def __post_init__(self):
        """Validación de consistencia física y lógica."""
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Dimensions must be positive")
        
        # El área de trabajo no puede exceder los límites físicos del hardware
        if self.width > self.max_x or self.height > self.max_y:
            raise ValueError(
                f"Work area ({self.width}x{self.height}) exceeds "
                f"physical limits ({self.max_x}x{self.max_y})"
            )
        
        if self.feedrate_draw <= 0 or self.feedrate_move <= 0:
            raise ValueError("Feedrates must be positive")

    @property
    def tool_up(self) -> ToolState:
        return ToolState.UP

    @property
    def tool_down(self) -> ToolState:
        return ToolState.DOWN
