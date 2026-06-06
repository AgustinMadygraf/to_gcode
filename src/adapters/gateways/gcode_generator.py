from typing import List, Optional, Dict
from src.application.boundaries.gateways import GCodeGenerator
from src.application.boundaries.infrastructure_interfaces import GCodeLibraryWrapper
from src.dominio.entidades.geometria import Trayectoria
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina
from src.dominio.servicios.geometry_service import GeometryService

class PyGCodeGenerator(GCodeGenerator):
    """
    Adaptador purificado para generación de G-Code. 
    Su única responsabilidad es traducir objetos del dominio a sintaxis técnica.
    """
    def __init__(
        self, 
        wrapper: GCodeLibraryWrapper, 
        geometry_service: GeometryService,
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
        return self.wrapper.format_line(command, params)

    def generate(self, paths: List[Trayectoria], config: ConfiguracionMaquina) -> str:
        self.last_modal_command = None
        
        gcode_lines: List[str] = [
            self.wrapper.format_line("G21") + " " + self.wrapper.get_comment("Units in mm"),
            self.wrapper.format_line("G90") + " " + self.wrapper.get_comment("Absolute coordinates"),
            self.wrapper.format_line("G0", {"F": config.feedrate_move}),
            self.wrapper.format_line("G1", {"F": config.feedrate_draw})
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
            arc = self.geometry_service.fit_arc(points, self.arc_tolerance)
            
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

        gcode_lines.append(self._format_modal("G0", {"X": 0, "Y": 0}) + " " + self.wrapper.get_comment("Return home"))

        filtered_lines = [line for line in gcode_lines if line]

        if self.truncate_limit and self.truncate_limit > 0:
            return '\n'.join(filtered_lines[:self.truncate_limit])
            
        return '\n'.join(filtered_lines)
