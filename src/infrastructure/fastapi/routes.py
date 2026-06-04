"""
Path: src/infrastructure/fastapi/routes.py
"""

from typing import Annotated
from fastapi import APIRouter, UploadFile, File, Depends
from pydantic import BaseModel
from src.adapters.controllers.gcode_controller import GCodeController
from src.infrastructure.fastapi.dependencies import get_gcode_controller

router = APIRouter()

class ConfigSchema(BaseModel):
    name: str
    width: float
    height: float
    pen_up_command: str
    pen_down_command: str
    feedrate_draw: float
    feedrate_move: float
    invert_y: bool = True
    scale_to_fit: bool = True

@router.post("/config", status_code=201)
def set_config(
    config: ConfigSchema, 
    controller: Annotated[GCodeController, Depends(get_gcode_controller)]
):
    return controller.set_config(config.model_dump())

@router.get("/config")
def get_config(controller: Annotated[GCodeController, Depends(get_gcode_controller)]):
    config = controller.get_config()
    return config

class UrlSchema(BaseModel):
    url: str

@router.post("/convert/url")
def convert_svg_url(
    data: UrlSchema,
    controller: Annotated[GCodeController, Depends(get_gcode_controller)]
):
    from urllib.request import urlopen
    with urlopen(data.url) as response:
        content = response.read().decode("utf-8")
    return controller.convert_svg(content)

@router.post("/convert")
async def convert_svg(
    file: Annotated[UploadFile, File()],
    controller: Annotated[GCodeController, Depends(get_gcode_controller)]
):
    content = await file.read()
    return controller.convert_svg(content.decode("utf-8"))
