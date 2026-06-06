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

        # Mapeo de columnas DB (nombres antiguos/técnicos) a nuevos campos del dominio
        # Asumiendo que la DB usa los nombres antiguos, necesitamos maparlos.
        # O podemos actualizar la DB, pero esto es un MVP.
        # Mejor mapear los datos leídos de la DB a los campos de la entidad.
        
        datos_mapeados = {
            "nombre": datos.get("nombre"),
            "ancho_area_trabajo": datos.get("ancho_area_trabajo", datos.get("ancho", 0.0)),
            "alto_area_trabajo": datos.get("alto_area_trabajo", datos.get("alto", 0.0)),
            "ancho_maximo_maquina": datos.get("ancho_maximo_maquina", datos.get("max_x", 0.0)),
            "alto_maximo_maquina": datos.get("alto_maximo_maquina", datos.get("max_y", 0.0)),
            "comando_pluma_arriba": datos.get("comando_pluma_arriba", datos.get("pen_up_comando", "M5")),
            "comando_pluma_abajo": datos.get("comando_pluma_abajo", datos.get("pen_down_comando", "M3")),
            "velocidad_dibujo": datos.get("velocidad_dibujo"),
            "velocidad_movimiento": datos.get("velocidad_movimiento"),
            "invertir_eje_y": datos.get("invertir_eje_y", datos.get("invertir_y", True)),
            "ajustar_a_escala": datos.get("ajustar_a_escala", datos.get("ajustar_a_escala", True)),
        }
            
        return ConfiguracionMaquina(**datos_mapeados)

    def guardar_configuracion(self, configuracion: ConfiguracionMaquina) -> None:
        datos: Dict[str, Any] = {
            "nombre": configuracion.nombre,
            "ancho_area_trabajo": configuracion.ancho_area_trabajo,
            "alto_area_trabajo": configuracion.alto_area_trabajo,
            "ancho_maximo_maquina": configuracion.ancho_maximo_maquina,
            "alto_maximo_maquina": configuracion.alto_maximo_maquina,
            "comando_pluma_arriba": configuracion.comando_pluma_arriba,
            "comando_pluma_abajo": configuracion.comando_pluma_abajo,
            "velocidad_dibujo": configuracion.velocidad_dibujo,
            "velocidad_movimiento": configuracion.velocidad_movimiento,
            "invertir_eje_y": configuracion.invertir_eje_y,
            "ajustar_a_escala": configuracion.ajustar_a_escala
        }
        self.proveedor.actualizar_o_insertar(configuracion.nombre, datos)
