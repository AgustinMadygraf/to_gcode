"""
Path: src/infrastructure/pygcode/wrapper.py
"""

import pygcode # type: ignore
from typing import Dict, Optional, List, Any
from src.application.boundaries.infrastructure_interfaces import GCodeLibraryWrapper

class PyGCodeWrapper(GCodeLibraryWrapper):
    def format_line(self, command: str, params: Optional[Dict[str, float]] = None) -> str:
        pg: Any = pygcode
        words: List[Any] = [pg.GCodeWord(command[0], int(command[1:]))]
        if params:
            for key, value in params.items():
                words.append(pg.GCodeWord(key, value))
        block = pg.GCodeBlock(words)
        return str(block)

    def get_comment(self, text: str) -> str:
        return f"; {text}"
