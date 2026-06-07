from typing import List
from src.aplicacion.casos_de_uso.convertidor_base import ConvertidorBaseGCode
from src.aplicacion.limites.puertos_casos_de_uso import PuertoConversionSVG
from src.aplicacion.limites.puertos import AnalizadorVectorial, GeneradorGCode
from src.aplicacion.limites.interfaz_repositorio_configuracion_maquina import RepositorioConfiguracionMaquina
from src.dominio.interfaces.optimizador_trayectoria import OptimizadorTrayectoria
from src.aplicacion.servicios.servicio_preparacion_trayectoria import ServicioPreparacionTrayectoria
from src.dominio.entidades.geometria import Trayectoria
from src.dominio.servicios.especificaciones_trayectoria import TrayectoriaNoVacia
from src.dominio.excepciones.base import ReglaDeNegocioVioladaError, ConfiguracionNoEncontradaError
from src.aplicacion.dto.solicitudes import ConversionSvgRequest
from src.dominio.interfaces.transformador_geometria import TransformadorGeometria

class ConvertirSVGAGCode(ConvertidorBaseGCode, PuertoConversionSVG):
    def __init__(
        self, 
        analizador: AnalizadorVectorial, 
        generador: GeneradorGCode, 
        repositorio: RepositorioConfiguracionMaquina,
        servicio_preparacion: ServicioPreparacionTrayectoria,
        optimizador: OptimizadorTrayectoria,
        transformador: TransformadorGeometria
    ):
        super().__init__(generador=generador, repositorio=repositorio, servicio_preparacion=servicio_preparacion, optimizador=optimizador)
        self.analizador = analizador
        self.transformador = transformador

    def ejecutar(self, datos_entrada: ConversionSvgRequest) -> str:
        # Invertir eje Y antes de la preparación estándar
        svg_content = datos_entrada.contenido_svg
        trayectorias = self._parsear_entrada(svg_content)
        trayectorias_invertidas = self.transformador.invertir_eje_y(trayectorias)
        
        # Ejecutar el resto del flujo normalmente (el método ejecutar original hace parsear_entrada de nuevo, 
        # necesitamos refactorizar el flujo si queremos ser limpios).
        
        # SOLUCIÓN RÁPIDA: sobreescribir ejecutar o refactorizar ConvertidorBase.
        # Dado el tiempo, ajustaremos la lógica aquí llamando a una ejecución de flujo directo.
        
        # Refactorización del flujo:
        config = self.repositorio.obtener_configuracion()
        if not config:
            raise ConfiguracionNoEncontradaError("Configuración no encontrada")
            
        trayectorias_transformadas = self.servicio_preparacion.preparar(trayectorias_invertidas, config)
        trayectorias_optimizadas = self.optimizador.optimizar(trayectorias_transformadas)
        return self.generador.generar(trayectorias_optimizadas, config)

    def _parsear_entrada(self, input_datos: str) -> List[Trayectoria]:
        trayectorias = self.analizador.parsear_svg(input_datos)
        
        validador = TrayectoriaNoVacia()
        for t in trayectorias:
            if not validador.es_satisfecha_por(t):
                raise ReglaDeNegocioVioladaError("Se encontró una trayectoria vacía en el SVG")
                
        return trayectorias
