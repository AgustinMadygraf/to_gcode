"""
Trayectoria: src/adaptadores/pasarelas/repositorio_configuracion_maquina_impl.py
"""
from typing import Optional, Dict, Any
from src.aplicacion.limites.interfaz_repositorio_configuracion_maquina import RepositorioConfiguracionMaquina
from src.adaptadores.pasarelas.envoltorios_tecnicos import ProveedorPersistenciaConfiguracion
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina

class RepositorioConfiguracionMaquinaSqlAlchemy(RepositorioConfiguracionMaquina):
    def __init__(self, proveedor: ProveedorPersistenciaConfiguracion):
        self.proveedor = proveedor

    def obtener_configuracion(self) -> Optional[ConfiguracionMaquina]:
        datos = self.proveedor.buscar_primero()
        if not datos:
            return None

        if 'max_x' not in datos:
            datos['max_x'] = datos.get('width', 0.0)
        if 'max_y' not in datos:
            datos['max_y'] = datos.get('height', 0.0)
            
        return ConfiguracionMaquina(**datos)

    def guardar_configuracion(self, configuracion: ConfiguracionMaquina) -> None:
        datos: Dict[str, Any] = {
            "width": configuracion.width,
            "height": configuracion.height,
            "max_x": configuracion.max_x,
            "max_y": configuracion.max_y,
            "pen_up_comando": configuracion.pen_up_comando,
            "pen_down_comando": configuracion.pen_down_comando,
            "feedrate_draw": configuracion.feedrate_draw,
            "feedrate_move": configuracion.feedrate_move,
            "invert_y": configuracion.invert_y,
            "scale_to_fit": configuracion.scale_to_fit
        }
        self.proveedor.actualizar_o_insertar(configuracion.nombre, datos)
