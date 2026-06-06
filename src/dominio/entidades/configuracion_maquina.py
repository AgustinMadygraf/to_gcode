"""
Path: src/dominio/entidades/configuracion_maquina.py
"""

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
    comando_anulado: Optional[str] = None # Solo para excepciones técnicas

VelocidadAvance = NewType('VelocidadAvance', float)

@dataclass(frozen=True)
class ConfiguracionMaquina:
    """Configuración de la máquina plotter con validación de consistencia física."""
    nombre: str
    ancho_area_trabajo: float
    alto_area_trabajo: float
    ancho_maximo_maquina: float
    alto_maximo_maquina: float
    comando_pluma_arriba: str
    comando_pluma_abajo: str
    velocidad_dibujo: VelocidadAvance
    velocidad_movimiento: VelocidadAvance
    invertir_eje_y: bool = True
    ajustar_a_escala: bool = True

    def __post_init__(self):
        """Validación de consistencia física y lógica."""
        if self.ancho_area_trabajo <= 0 or self.alto_area_trabajo <= 0:
            raise ValueError("Las dimensiones deben ser positivas")
        
        # El área de trabajo no puede exceder los límites físicos del hardware
        if self.ancho_area_trabajo > self.ancho_maximo_maquina or self.alto_area_trabajo > self.alto_maximo_maquina:
            raise ValueError(
                f"El área de trabajo ({self.ancho_area_trabajo}x{self.alto_area_trabajo}) excede "
                f"los límites físicos ({self.ancho_maximo_maquina}x{self.alto_maximo_maquina})"
            )
        
        if self.velocidad_dibujo <= 0 or self.velocidad_movimiento <= 0:
            raise ValueError("Las velocidades de avance deben ser positivas")

    @property
    def herramienta_arriba(self) -> EstadoHerramienta:
        return EstadoHerramienta.ARRIBA

    @property
    def herramienta_abajo(self) -> EstadoHerramienta:
        return EstadoHerramienta.ABAJO
