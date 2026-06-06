"""
Path: src/adapters/gateways/gcode_generator.py
"""

from typing import Dict, List, Optional
from src.aplicacion.limites.puertos import GeneradorGCode
from src.aplicacion.limites.interfaces_infraestructura import EnvoltorioLibreriaGCode
from src.dominio.entidades.geometria import Trayectoria
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina
from src.dominio.servicios.servicio_geometria import ServicioGeometria

class PyGeneradorGCode(GeneradorGCode):
    """
    Adaptador purificado para generación de G-Code. 
    Su única responsabilidad es traducir objetos del dominio a sintaxis técnica.
    """
    def __init__(
        self, 
        wrapper: EnvoltorioLibreriaGCode, 
        geometry_service: ServicioGeometria,
        truncate_limit: Optional[int] = None,
        arc_tolerance: float = 2.0
    ):
        self.wrapper = wrapper
        self.geometry_service = geometry_service
        self.truncate_limit = truncate_limit
        self.arc_tolerance = arc_tolerance
        self.last_modal_command: Optional[str] = None

    def _format_modal(self, command: str, params: Optional[Dict[str, float]] = None) -> str:
        """Maneja comandos modales de G-Code (G0, G1, etc.) para evitar repeticiones."""
        if command == self.last_modal_command:
            if params:
                return " ".join([f"{k}{v:.3f}" for k, v in params.items()])
            return ""

        self.last_modal_command = command
        return self.wrapper.formatear_linea(command, params)

    def generar(self, paths: List[Trayectoria], config: ConfiguracionMaquina) -> str:
        self.last_modal_command = None
        
        gcode_lines: List[str] = [
            self.wrapper.formatear_linea("G21") + " " + self.wrapper.obtener_comentario("Units in mm"),
            self.wrapper.formatear_linea("G90") + " " + self.wrapper.obtener_comentario("Absolute coordinates"),
            self.wrapper.formatear_linea("G0", {"F": config.feedrate_move}),
            self.wrapper.formatear_linea("G1", {"F": config.feedrate_draw})
        ]

        self.last_modal_command = "G1" 

        for path in paths:
            if path.es_vacia:
                continue

            # La simplificación ahora es responsabilidad del dominio
            domain_path = path.simplificada()
            points = domain_path.puntos
            
            # Orquestación de traducción a G-Code
            gcode_lines.append(config.pen_up_command)
            gcode_lines.append(self._format_modal("G0", {"X": points[0].x, "Y": points[0].y}))
            gcode_lines.append(config.pen_down_command)

            # Intento de ajuste de arco (Lógica de dominio vía servicio)
            arc = self.geometry_service.ajustar_arco(points, self.arc_tolerance)
            
            if arc:
                gcode_lines.append(self._format_modal("G2", {
                    "X": arc.punto_fin.x, 
                    "Y": arc.punto_fin.y, 
                    "I": arc.centro.x - arc.punto_inicio.x, 
                    "J": arc.centro.y - arc.punto_inicio.y
                }))
            else:
                for p in points[1:]:
                    gcode_lines.append(self._format_modal("G1", {"X": p.x, "Y": p.y}))
            
            gcode_lines.append(config.pen_up_command)

        gcode_lines.append(self._format_modal("G0", {"X": 0, "Y": 0}) + " " + self.wrapper.obtener_comentario("Return home"))

        filtered_lines = [line for line in gcode_lines if line]

        if self.truncate_limit and self.truncate_limit > 0:
            return '\n'.join(filtered_lines[:self.truncate_limit])
            
        return '\n'.join(filtered_lines)
