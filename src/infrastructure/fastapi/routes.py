from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from src.adapters.controladores.controlador_gcode import ControladorGCode
from src.infrastructure.fastapi.dependencies import get_controlador_gcode
from src.infrastructure.pydantic.schemas import ConfigSchema, UrlSchema
from src.infrastructure.settings.logger import logger
import httpx

router = APIRouter()

@router.post("/config", status_code=201)
def set_config(
    config: ConfigSchema,
    controller: ControladorGCode = Depends(get_controlador_gcode)
):
    try:
        data = config.model_dump()
        # Normalización técnica pre-entrada al núcleo
        if data.get('max_x') is None or data.get('max_x') == 0:
            data['max_x'] = data.get('width')
        if data.get('max_y') is None or data.get('max_y') == 0:
            data['max_y'] = data.get('height')
            
        return controller.set_config(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/config")
def obtener_configuracion(controller: ControladorGCode = Depends(get_controlador_gcode)):
    config_output = controller.obtener_configuracion()
    if not config_output:
        raise HTTPException(status_code=404, detail="Config not found")
    return config_output

@router.post("/convert")
async def convert_svg(
    file: UploadFile = File(...),
    controller: ControladorGCode = Depends(get_controlador_gcode)
):
    if not file.filename or not file.filename.endswith('.svg'):
        raise HTTPException(status_code=400, detail="Only SVG files allowed")
    
    content = await file.read()
    try:
        return controller.convert_svg(content.decode("utf-8"))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/convert/image")
async def convert_image(
    file: UploadFile = File(...),
    controller: ControladorGCode = Depends(get_controlador_gcode)
):
    content = await file.read()
    try:
        return controller.convert_image(content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/convert/url")
async def convert_url(
    payload: UrlSchema,
    controller: ControladorGCode = Depends(get_controlador_gcode)
):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(payload.url)
            response.raise_for_status()
            content = response.text
            return controller.convert_svg(content)
        except Exception as e:
            logger.error(f"Error fetching SVG from URL: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Could not fetch SVG from URL: {str(e)}")
