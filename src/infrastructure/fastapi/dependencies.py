from typing import Generator, Any
from fastapi import Depends

from src.infrastructure.settings.config import settings
from src.infrastructure.database.persistence_impl import SQLAlchemyConfigProvider
from src.infrastructure.database.session_provider import SqlAlchemySessionProvider
from src.adapters.gateways.machine_config_repository import SQLAlchemyMachineConfigRepository
from src.infrastructure.svgpathtools.wrapper import SvgPathToolsWrapper
from src.infrastructure.image_processing.raster_wrapper import ScikitImageWrapper
from src.infrastructure.pygcode.wrapper import PyGCodeWrapper
from src.adapters.gateways.svg_parser import SvgPathToolsParser
from src.adapters.gateways.raster_parser import RasterParser
from src.adapters.gateways.gcode_generator import PyGCodeGenerator
from src.domain.services.geometry_service import GeometryService
from src.domain.services.path_optimizer import GreedyPathOptimizer
from src.application.services.path_preparation_service import PathPreparationService
from src.application.use_cases.convert_svg import ConvertSVGToGCode
from src.application.use_cases.convert_image import ConvertImageToGCode
from src.adapters.controllers.gcode_controller import GCodeController
from src.application.boundaries.infrastructure_interfaces import DatabaseSessionProvider
from src.infrastructure.numpy.skeleton_wrapper import NumpySkeletonWrapper
from src.infrastructure.math.geometry_wrapper import GeometryWrapper
from src.infrastructure.math.geometry_transformer_impl import GeometryTransformerImpl
from src.infrastructure.math.diamond_pattern_generator import DiamondPatternGenerator

def get_session_provider() -> DatabaseSessionProvider:
    return SqlAlchemySessionProvider()

def get_db(provider: DatabaseSessionProvider = Depends(get_session_provider)) -> Generator[Any, None, None]:
    yield from provider.get_session()

def get_gcode_controller(db: Any = Depends(get_db)) -> GCodeController:
    persistence_provider = SQLAlchemyConfigProvider(db)

    # Dominio y Servicios base
    geom_processor = GeometryWrapper()
    geom_service = GeometryService(geometry_processor=geom_processor)
    
    geometry_transformer = GeometryTransformerImpl()
    pattern_generator = DiamondPatternGenerator()
    path_optimizer = GreedyPathOptimizer()

    # Servicios de Aplicación
    prep_service = PathPreparationService(
        transformer=geometry_transformer, 
        pattern_generator=pattern_generator
    )

    # Infraestructura / Gateways
    gcode_wrapper = PyGCodeWrapper()
    generator = PyGCodeGenerator(
        wrapper=gcode_wrapper, 
        geometry_service=geom_service, 
        truncate_limit=settings.GCODE_TRUNCATE_LIMIT, 
        arc_tolerance=settings.ARC_TOLERANCE
    )
    
    repo = SQLAlchemyMachineConfigRepository(provider=persistence_provider)

    # Caso de Uso SVG
    svg_wrapper = SvgPathToolsWrapper()
    svg_parser = SvgPathToolsParser(wrapper=svg_wrapper)
    svg_converter = ConvertSVGToGCode(
        parser=svg_parser, 
        generator=generator, 
        repo=repo, 
        preparation_service=prep_service,
        optimizer=path_optimizer
    )

    # Caso de Uso Imagen
    raster_processor = ScikitImageWrapper(skeleton_wrapper_factory=NumpySkeletonWrapper)
    raster_parser = RasterParser(processor=raster_processor)
    image_converter = ConvertImageToGCode(
        parser=raster_parser, 
        generator=generator, 
        repo=repo, 
        preparation_service=prep_service,
        optimizer=path_optimizer
    )
    
    return GCodeController(svg_converter=svg_converter, image_converter=image_converter, repo=repo)
