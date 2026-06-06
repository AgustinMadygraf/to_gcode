from pydantic import BaseModel

class ConfigSchema(BaseModel):
    nombre: str
    width: float
    height: float
    max_x: float
    max_y: float
    pen_up_comando: str
    pen_down_comando: str
    feedrate_draw: float
    feedrate_move: float
    invert_y: bool = True
    scale_to_fit: bool = True

class UrlSchema(BaseModel):
    url: str
