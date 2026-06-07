"""
Path: src/aplicacion/dto/solicitudes.py
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class ConversionSvgRequest:
    contenido_svg: str
