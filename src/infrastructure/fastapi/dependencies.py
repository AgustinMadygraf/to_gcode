"""
Path: src/infrastructure/fastapi/dependencies.py
"""

from typing import Generator, Any
from fastapi import Depends

from src.infrastructure.settings.config import settings
from src.infrastructure.database.persistence_impl import SQLAlchemyConfigProvider
from src.infrastructure.database.session_provider import SqlAlchemySessionProvider
from src.adapters.gateways.implementacion_repositorio_configuracion_maquina import SQLAlchemyRepositorioConfiguracionMaquina
from src.infrastructure.svgpathtools.envoltorio_svg import SvgTrayectoriaToolsWrapper
from src.infrastructure.image_processing.raster_wrapper import ScikitImageWrapper
from src.infrastructure.pygcode.envoltorio_gcode import PyGCodeWrapper
from src.adapters.gateways.svg_parser import SvgTrayectoriaToolsParser
from src.adapters.gateways.raster_parser import AnalizadorRaster
from src.adapters.gateways.gcode_generator import PyGeneradorGCode
from src.dominio.servicios.servicio_geometria import ServicioGeometria
from src.dominio.servicios.servicio_optimizador_trayectoria import OptimizadorTrayectoriaVoraz
from src.aplicacion.servicios.servicio_preparacion_trayectoria import ServicioPreparacionTrayectoria
from src.aplicacion.casos_de_uso.convertir_svg import ConvertirSVGAGCode
from src.aplicacion.casos_de_uso.convertir_imagen import ConvertirImagenAGCode
from src.adapters.controllers.gcode_controller import GCodeController
from src.adapters.gateways.envoltorios_tecnicos import ProveedorSesionBaseDatos
from src.infrastructure.numpy.skeleton_wrapper import NumpySkeletonWrapper
from src.infrastructure.math.geometry_wrapper import EnvoltorioGeometria
from src.infrastructure.math.geometry_transformer_impl import ImplementacionTransformadorGeometria
from src.infrastructure.math.diamond_pattern_generator import DiamondPatternGenerator as GeneradorPatronesDiamante


def obtener_sesion_provider() -> ProveedorSesionBaseDatos:
    return SqlAlchemySessionProvider()

def get_db(provider: ProveedorSesionBaseDatos = Depends(obtener_sesion_provider)) -> Generator[Any, None, None]:
    yield from provider.obtener_sesion()

def get_gcode_controller(db: Any = Depends(get_db)) -> GCodeController:
    persistence_provider = SQLAlchemyConfigProvider(db)

    geom_processor = EnvoltorioGeometria()
    geom_service = ServicioGeometria(procesador_geometria=geom_processor)
    
    geometry_transformer = ImplementacionTransformadorGeometria()
    pattern_generator = GeneradorPatronesDiamante()
    path_optimizer = OptimizadorTrayectoriaVoraz()

    prep_service = ServicioPreparacionTrayectoria(
        transformador=geometry_transformer, 
        generador_patrones=pattern_generator
    )

    gcode_wrapper = PyGCodeWrapper()
    generator = PyGeneradorGCode(
        wrapper=gcode_wrapper, 
        geometry_service=geom_service, 
        truncate_limit=settings.GCODE_TRUNCATE_LIMIT, 
        arc_tolerance=settings.ARC_TOLERANCE
    )

    repo = SQLAlchemyRepositorioConfiguracionMaquina(provider=persistence_provider)

    svg_wrapper = SvgTrayectoriaToolsWrapper()
    svg_parser = SvgTrayectoriaToolsParser(wrapper=svg_wrapper)
    svg_converter = ConvertirSVGAGCode(
        analizador=svg_parser, 
        generador=generator, 
        repositorio=repo, 
        servicio_preparacion=prep_service,
        optimizador=path_optimizer
    )

    raster_processor = ScikitImageWrapper(skeleton_wrapper_factory=NumpySkeletonWrapper)
    raster_parser = AnalizadorRaster(processor=raster_processor)
    image_converter = ConvertirImagenAGCode(
        analizador=raster_parser, 
        generador=generator, 
        repositorio=repo, 
        servicio_preparacion=prep_service,
        optimizador=path_optimizer
    )
    
    return GCodeController(svg_converter=svg_converter, image_converter=image_converter, repositorio=repo)
