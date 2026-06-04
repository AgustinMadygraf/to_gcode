"""
Path: src/infrastructure/settings/logger.py
"""

import logging
import sys
from src.infrastructure.settings.config import settings

def setup_logging():
    log_format = "%(levelname)s:     %(message)s"
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    logging.basicConfig(
        level=log_level,
        format=log_format,
        stream=sys.stdout,
        force=True
    )
    
    logger = logging.getLogger("to_gcode")
    return logger
logger = setup_logging()
