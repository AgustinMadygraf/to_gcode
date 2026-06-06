from typing import Optional, Dict, Any
from src.aplicacion.limites.interfaz_repositorio_configuracion_maquina import RepositorioConfiguracionMaquina
from src.adaptadores.pasarelas.envoltorios_tecnicos import ProveedorPersistenciaConfiguracion
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina
from src.infrastructure.database.models import ConfiguracionMaquinaModel

class SQLAlchemyConfigProvider(ProveedorPersistenciaConfiguracion):
    def __init__(self, session: Any):
        self.session = session

    def buscar_primero(self) -> Optional[Dict[str, Any]]:
        model = self.session.query(ConfiguracionMaquinaModel).first()
        if not model:
            return None
        
        # Convertir objeto SQLAlchemy a dict
        return {
            "nombre": model.nombre,
            "ancho_area_trabajo": model.ancho_area_trabajo,
            "alto_area_trabajo": model.alto_area_trabajo,
            "ancho_maximo_maquina": model.ancho_maximo_maquina,
            "alto_maximo_maquina": model.alto_maximo_maquina,
            "comando_pluma_arriba": model.comando_pluma_arriba,
            "comando_pluma_abajo": model.comando_pluma_abajo,
            "velocidad_dibujo": model.velocidad_dibujo,
            "velocidad_movimiento": model.velocidad_movimiento,
            "invertir_eje_y": model.invertir_eje_y,
            "ajustar_a_escala": model.ajustar_a_escala
        }

    def actualizar_o_insertar(self, nombre: str, datos: Dict[str, Any]) -> None:
        model = self.session.query(ConfiguracionMaquinaModel).filter_by(nombre=nombre).first()
        if model:
            for key, value in datos.items():
                setattr(model, key, value)
        else:
            model = ConfiguracionMaquinaModel(nombre=nombre, **datos)
            self.session.add(model)
        self.session.commit()
