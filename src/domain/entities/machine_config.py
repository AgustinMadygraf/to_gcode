"""
Path: src/domain/entities/machine_config.py
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class MachineConfig:
    "Configuración de la máquina plotter."
    name: str
    width: float
    height: float
    pen_up_command: str  # Ejemplo: 'M5'
    pen_down_command: str  # Ejemplo: 'M3 S1000'
    feedrate_draw: float  # Velocidad de dibujo (G1)
    feedrate_move: float  # Velocidad de movimiento en vacío (G0)
    invert_y: bool = True  # Y_gcode = height - Y_svg
    scale_to_fit: bool = True  # Escalado proporcional automático

@dataclass(frozen=True)
class Point:
    """Punto en el plano 2D."""
    x: float
    y: float

@dataclass(frozen=True)
class Path:
    """Ruta compuesta por una serie de puntos."""
    points: list[Point]
