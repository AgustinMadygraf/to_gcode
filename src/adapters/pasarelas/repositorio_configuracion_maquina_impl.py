"""
Trayectoria: src/adapters.pasarelas/machine_config_repository.py
"""
from typing import Optional, Dict, Any
from src.aplicacion.limites.interfaz_repositorio_configuracion_maquina import RepositorioConfiguracionMaquina
from src.adapters.pasarelas.envoltorios_tecnicos import ProveedorPersistenciaConfiguracion
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina

class SQLAlchemyRepositorioConfiguracionMaquina(RepositorioConfiguracionMaquina):
    def __init__(self, provider: ProveedorPersistenciaConfiguracion):
        self.provider = provider

    def obtener_configuracion(self) -> Optional[ConfiguracionMaquina]:
        data = self.provider.buscar_primero()
        if not data:
            return None

        if 'max_x' not in data:
            data['max_x'] = data.get('width', 0.0)
        if 'max_y' not in data:
            data['max_y'] = data.get('height', 0.0)
            
        return ConfiguracionMaquina(**data)

    def guardar_configuracion(self, config: ConfiguracionMaquina) -> None:
        data: Dict[str, Any] = {
            "width": config.width,
            "height": config.height,
            "max_x": config.max_x,
            "max_y": config.max_y,
            "pen_up_command": config.pen_up_command,
            "pen_down_command": config.pen_down_command,
            "feedrate_draw": config.feedrate_draw,
            "feedrate_move": config.feedrate_move,
            "invert_y": config.invert_y,
            "scale_to_fit": config.scale_to_fit
        }
        self.provider.actualizar_o_insertar(config.name, data)
