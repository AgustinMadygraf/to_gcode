"""
Path: src/infrastructure/pygcode/wrapper.py
"""

import pygcode # type: ignore
from typing import Dict, Optional, Any
from src.application.boundaries.infrastructure_interfaces import GCodeLibraryWrapper

class PyGCodeWrapper(GCodeLibraryWrapper):
    def format_line(self, command: str, params: Optional[Dict[str, float]] = None) -> str:
        pg: Any = pygcode
        
        # Separamos la velocidad de las coordenadas si existe
        feedrate = params.pop('F', None) if params else None
        
        if command == "G0":
            line = pg.gcodes.GCodeRapidMove(**(params or {}))
        elif command == "G1":
            line = pg.gcodes.GCodeLinearMove(**(params or {}))
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

    def get_comment(self, text: str) -> str:
        return f"; {text}"
