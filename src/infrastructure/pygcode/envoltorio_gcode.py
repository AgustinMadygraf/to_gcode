"""
Trayectoria: src/infrastructure/pygcode/wrapper.py
"""

import pygcode # type: ignore
from typing import Dict, Optional, Any
from src.adapters.pasarelas.envoltorios_tecnicos import EnvoltorioLibreriaGCode

class PyGCodeWrapper(EnvoltorioLibreriaGCode):
    def formatear_linea(self, command: str, params: Optional[Dict[str, float]] = None) -> str:
        pg: Any = pygcode
        
        # Separamos la velocidad de las coordenadas si existe
        feedrate = params.pop('F', None) if params else None
        
        if command == "G0":
            line = pg.gcodes.GCodeRapidMove(**(params or {}))
        elif command == "G1":
            line = pg.gcodes.GCodeLinearMove(**(params or {}))
        elif command == "G2":
            line = pg.gcodes.GCodeArcMoveCW(**(params or {}))
        elif command == "G3":
            line = pg.gcodes.GCodeArcMoveCCW(**(params or {}))
        elif command == "G21":
            line = pg.gcodes.GCodeUseMillimeters()
        elif command == "G90":
            line = pg.gcodes.GCodeAbsoluteDistanceMode()
        else:
            return f"{command} " + " ".join([f"{k}{v:.3f}" for k, v in (params or {}).items()])

        result = str(line)
        
        # Si había velocidad, añadimos un comando G1 adicional o concatenamos si la librería lo permite
        if feedrate is not None:
            result += f" F{feedrate:.3f}"
            
        return result

    def obtener_comentario(self, text: str) -> str:
        return f"; {text}"
