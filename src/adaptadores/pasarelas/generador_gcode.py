"""
Path: src/adapters.pasarelas/gcode_generator.py
"""

from typing import Dict, List, Optional
from src.aplicacion.limites.puertos import GeneradorGCode
from src.adaptadores.pasarelas.envoltorios_tecnicos import EnvoltorioLibreriaGCode
from src.dominio.entidades.geometria import Trayectoria
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina
from src.dominio.servicios.servicio_geometria import ServicioGeometria

class GeneradorGCodePy(GeneradorGCode):
    def __init__(
        self, 
        envoltorio: EnvoltorioLibreriaGCode, 
        servicio_geometria: ServicioGeometria,
        limite_truncado: Optional[int] = None,
        tolerancia_arco: float = 2.0
    ):
        self.envoltorio = envoltorio
        self.servicio_geometria = servicio_geometria
        self.limite_truncado = limite_truncado
        self.tolerancia_arco = tolerancia_arco
        self.ultimo_comando_modal: Optional[str] = None

    def _formatear_modal(self, comando: str, parametros: Optional[Dict[str, float]] = None) -> str:
        if comando == self.ultimo_comando_modal:
            if parametros:
                return " ".join([f"{k}{v:.3f}" for k, v in parametros.items()])
            return ""

        self.ultimo_comando_modal = comando
        return self.envoltorio.formatear_linea(comando, parametros)

    def generar(self, trayectorias: List[Trayectoria], config: ConfiguracionMaquina) -> str:
        self.ultimo_comando_modal = None
        
        gcode_lines: List[str] = [
            self.envoltorio.formatear_linea("G21") + " " + self.envoltorio.obtener_comentario("Unidades en mm"),
            self.envoltorio.formatear_linea("G90") + " " + self.envoltorio.obtener_comentario("Coordenadas absolutas"),
            self.envoltorio.formatear_linea("G0", {"F": config.velocidad_movimiento}),
            self.envoltorio.formatear_linea("G1", {"F": config.velocidad_dibujo})
        ]

        self.ultimo_comando_modal = "G1" 

        for trayectoria in trayectorias:
            if trayectoria.es_vacia:
                continue

            # La simplificación ahora es responsabilidad del dominio
            domain_path = trayectoria.simplificada()
            points = domain_path.puntos
            
            # Orquestación de traducción a G-Code
            gcode_lines.append(config.comando_pluma_arriba)
            gcode_lines.append(self._formatear_modal("G0", {"X": points[0].x, "Y": points[0].y}))
            gcode_lines.append(config.comando_pluma_abajo)

            # Intento de ajuste de arco (Lógica de dominio vía servicio)
            arc = self.servicio_geometria.ajustar_arco(points, self.tolerancia_arco)
            
            if arc:
                gcode_lines.append(self._formatear_modal("G2", {
                    "X": arc.punto_fin.x, 
                    "Y": arc.punto_fin.y, 
                    "I": arc.centro.x - arc.punto_inicio.x, 
                    "J": arc.centro.y - arc.punto_inicio.y
                }))
            else:
                for p in points[1:]:
                    gcode_lines.append(self._formatear_modal("G1", {"X": p.x, "Y": p.y}))
            
            gcode_lines.append(config.comando_pluma_arriba)

        gcode_lines.append(self._formatear_modal("G0", {"X": 0, "Y": 0}) + " " + self.envoltorio.obtener_comentario("Return home"))

        filtered_lines = [line for line in gcode_lines if line]

        if self.limite_truncado and self.limite_truncado > 0:
            return '\n'.join(filtered_lines[:self.limite_truncado])
            
        return '\n'.join(filtered_lines)
