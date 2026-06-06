from pydantic import BaseModel

class ConfigSchema(BaseModel):
    nombre: str
    ancho_area_trabajo: float
    alto_area_trabajo: float
    ancho_maximo_maquina: float
    alto_maximo_maquina: float
    comando_pluma_arriba: str
    comando_pluma_abajo: str
    velocidad_dibujo: float
    velocidad_movimiento: float
    invertir_eje_y: bool = True
    ajustar_a_escala: bool = True

class UrlSchema(BaseModel):
    url: str
