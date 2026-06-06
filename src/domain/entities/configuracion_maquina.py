from dataclasses import dataclass
from enum import Enum
from typing import NewType, Optional

# Abstracción semántica de la herramienta
class EstadoHerramienta(Enum):
    ARRIBA = "UP"
    ABAJO = "DOWN"

@dataclass(frozen=True)
class AccionHerramienta:
    """Representa una acción de la herramienta sin depender de strings G-Code."""
    estado: EstadoHerramienta
    comando_override: Optional[str] = None # Solo para excepciones técnicas

VelocidadAvance = NewType('VelocidadAvance', float)

@dataclass(frozen=True)
class ConfiguracionMaquina:
    """Configuración de la máquina plotter con validación de consistencia física."""
    name: str
    width: float   # Área de trabajo lógica
    height: float  # Área de trabajo lógica
    max_x: float   # Límite físico hardware
    max_y: float   # Límite físico hardware
    pen_up_command: str   # Se mantiene para infraestructura pero el dominio usará EstadoHerramienta
    pen_down_command: str
    feedrate_draw: VelocidadAvance
    feedrate_move: VelocidadAvance
    invert_y: bool = True
    scale_to_fit: bool = True

    def __post_init__(self):
        """Validación de consistencia física y lógica."""
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Las dimensiones deben ser positivas")
        
        # El área de trabajo no puede exceder los límites físicos del hardware
        if self.width > self.max_x or self.height > self.max_y:
            raise ValueError(
                f"El área de trabajo ({self.width}x{self.height}) excede "
                f"los límites físicos ({self.max_x}x{self.max_y})"
            )
        
        if self.feedrate_draw <= 0 or self.feedrate_move <= 0:
            raise ValueError("Las velocidades de avance deben ser positivas")

    @property
    def herramienta_arriba(self) -> EstadoHerramienta:
        return EstadoHerramienta.ARRIBA

    @property
    def herramienta_abajo(self) -> EstadoHerramienta:
        return EstadoHerramienta.ABAJO
