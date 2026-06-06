from src.aplicacion.limites.puertos_casos_de_uso import PuertoGestionConfiguracion
from src.aplicacion.limites.puertos_casos_de_uso import PuertoGestionConfiguracion
from typing import Dict, Any, Optional
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina
from src.aplicacion.limites.interfaz_repositorio_configuracion_maquina import RepositorioConfiguracionMaquina

class GestionarConfiguracion(PuertoGestionConfiguracion):
    def __init__(self, repositorio: RepositorioConfiguracionMaquina):
        self.repositorio = repositorio

    def guardar(self, config_datos: Dict[str, Any]) -> None:
        entity = ConfiguracionMaquina(**config_datos)
        self.repositorio.guardar_configuracion(entity)

    def obtener(self) -> Optional[ConfiguracionMaquina]:
        return self.repositorio.obtener_configuracion()
