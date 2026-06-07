from typing import Generator, Any
from fastapi import Depends

from src.infrastructure.settings.config import settings
from src.infrastructure.database.persistence_impl import SQLAlchemyConfigProvider
from src.infrastructure.database.session_provider import SqlAlchemySessionProvider
from src.adaptadores.pasarelas.repositorio_configuracion_maquina_impl import RepositorioConfiguracionMaquinaSqlAlchemy
from src.infrastructure.svgpathtools.envoltorio_svg import SvgTrayectoriaToolsWrapper
from src.infrastructure.image_processing.raster_wrapper import ScikitImageWrapper
from src.infrastructure.pygcode.envoltorio_gcode import PyGCodeWrapper
from src.adaptadores.pasarelas.analizador_svg import AnalizadorSvgToolsTrayectoria
from src.adaptadores.pasarelas.analizador_raster import AnalizadorRaster
from src.adaptadores.pasarelas.generador_gcode import GeneradorGCodePy
from src.dominio.servicios.servicio_geometria import ServicioGeometria
from src.dominio.servicios.servicio_optimizador_trayectoria import OptimizadorTrayectoriaVoraz
from src.aplicacion.servicios.servicio_preparacion_trayectoria import ServicioPreparacionTrayectoria
from src.aplicacion.casos_de_uso.convertir_svg import ConvertirSVGAGCode
from src.aplicacion.casos_de_uso.convertir_imagen import ConvertirImagenAGCode
from src.aplicacion.casos_de_uso.gestionar_configuracion import GestionarConfiguracion
from src.adaptadores.controladores.controlador_codigo_g import ControladorCodigoG
from src.adaptadores.pasarelas.envoltorios_tecnicos import ProveedorSesionBaseDatos
from src.infrastructure.numpy.skeleton_wrapper import NumpySkeletonWrapper
from src.infrastructure.math.geometry_wrapper import EnvoltorioGeometria
from src.infrastructure.math.geometry_transformer_impl import ImplementacionTransformadorGeometria
from src.infrastructure.math.diamond_pattern_generator import DiamondPatternGenerator as GeneradorPatronesDiamante


def obtener_sesion_provider() -> ProveedorSesionBaseDatos:
    return SqlAlchemySessionProvider()

def get_db(provider: ProveedorSesionBaseDatos = Depends(obtener_sesion_provider)) -> Generator[Any, None, None]:
    yield from provider.obtener_sesion()

def get_controlador_codigo_g(db: Any = Depends(get_db)) -> ControladorCodigoG:
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
    generator = GeneradorGCodePy(
        envoltorio=gcode_wrapper, 
        servicio_geometria=geom_service, 
        limite_truncado=settings.GCODE_TRUNCATE_LIMIT, 
        tolerancia_arco=settings.ARC_TOLERANCE
    )

    repo = RepositorioConfiguracionMaquinaSqlAlchemy(proveedor=persistence_provider)

    svg_wrapper = SvgTrayectoriaToolsWrapper()
    svg_parser = AnalizadorSvgToolsTrayectoria(envoltorio=svg_wrapper)
    svg_converter = ConvertirSVGAGCode(
        analizador=svg_parser, 
        generador=generator, 
        repositorio=repo, 
        servicio_preparacion=prep_service,
        optimizador=path_optimizer, transformador=geometry_transformer
    )

    raster_processor = ScikitImageWrapper(skeleton_wrapper_factory=NumpySkeletonWrapper)
    raster_parser = AnalizadorRaster(procesador=raster_processor)
    image_converter = ConvertirImagenAGCode(
        analizador=raster_parser, 
        generador=generator, 
        repositorio=repo, 
        servicio_preparacion=prep_service,
        optimizador=path_optimizer
    )
    
    gestor_configuracion = GestionarConfiguracion(repositorio=repo)
    
    return ControladorCodigoG(conversor_svg=svg_converter, conversor_imagen=image_converter, gestor_configuracion=gestor_configuracion)
