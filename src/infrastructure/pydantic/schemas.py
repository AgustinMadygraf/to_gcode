from pydantic import BaseModel

class ConfigSchema(BaseModel):
    name: str
    width: float
    height: float
    max_x: float
    max_y: float
    pen_up_command: str
    pen_down_command: str
    feedrate_draw: float
    feedrate_move: float
    invert_y: bool = True
    scale_to_fit: bool = True

class UrlSchema(BaseModel):
    url: str
