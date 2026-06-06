"""
Trayectoria: src/infrastructure/pygcode/wrapper.py
"""

import pygcode # type: ignore
from typing import Dict, Optional, Any
from src.adaptadores.pasarelas.envoltorios_tecnicos import EnvoltorioLibreriaGCode

class PyGCodeWrapper(EnvoltorioLibreriaGCode):
    def formatear_linea(self, comando: str, parametros: Optional[Dict[str, float]] = None) -> str:
        pg: Any = pygcode
        
        # Separamos la velocidad de las coordenadas si existe
        feedrate = parametros.pop('F', None) if parametros else None
        
        if comando == "G0":
            line = pg.gcodes.GCodeRapidMove(**(parametros or {}))
        elif comando == "G1":
            line = pg.gcodes.GCodeLinearMove(**(parametros or {}))
        elif comando == "G2":
            line = pg.gcodes.GCodeArcMoveCW(**(parametros or {}))
        elif comando == "G3":
            line = pg.gcodes.GCodeArcMoveCCW(**(parametros or {}))
        elif comando == "G21":
            line = pg.gcodes.GCodeUseMillimeters()
        elif comando == "G90":
            line = pg.gcodes.GCodeAbsoluteDistanceMode()
        else:
            return f"{comando} " + " ".join([f"{k}{v:.3f}" for k, v in (parametros or {}).items()])

        result = str(line)
        
        # Si había velocidad, añadimos un comando G1 adicional o concatenamos si la librería lo permite
        if feedrate is not None:
            result += f" F{feedrate:.3f}"
            
        return result

    def obtener_comentario(self, texto: str) -> str:
        return f"; {texto}"
