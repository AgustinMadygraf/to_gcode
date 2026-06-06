"""
Path: src/infrastructure/svgpathtools/envoltorio_svg.py
"""

from pydantic import BaseModel, Field

class ConfigSchema(BaseModel):
    nombre: str
    ancho_area_trabajo: float = Field(..., gt=0)
    alto_area_trabajo: float = Field(..., gt=0)
    ancho_maximo_maquina: float = Field(..., gt=0)
    alto_maximo_maquina: float = Field(..., gt=0)
    comando_pluma_arriba: str
    comando_pluma_abajo: str
    velocidad_dibujo: float = Field(..., gt=0)
    velocidad_movimiento: float = Field(..., gt=0)
    invertir_eje_y: bool = True
    ajustar_a_escala: bool = True

class UrlSchema(BaseModel):
    url: str
