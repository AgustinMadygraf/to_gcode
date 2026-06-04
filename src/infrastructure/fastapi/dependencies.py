"""
Path: src/infrastructure/fastapi/dependencies.py
"""

from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends

from src.infrastructure.database.models import SessionLocal
from src.infrastructure.database.persistence_impl import SQLAlchemyConfigProvider
from src.adapters.gateways.machine_config_repository import SQLAlchemyMachineConfigRepository
from src.infrastructure.svgpathtools.wrapper import SvgPathToolsWrapper
from src.infrastructure.pygcode.wrapper import PyGCodeWrapper
from src.adapters.gateways.svg_parser import SvgPathToolsParser
from src.adapters.gateways.gcode_generator import PyGCodeGenerator
from src.domain.services.geometry_service import GeometryService
from src.application.use_cases.convert_svg import ConvertSVGToGCode
from src.adapters.controllers.gcode_controller import GCodeController

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_gcode_controller(db: Session = Depends(get_db)) -> GCodeController:
    persistence_provider = SQLAlchemyConfigProvider(db)
    svg_wrapper = SvgPathToolsWrapper()
    gcode_wrapper = PyGCodeWrapper()
    
    repo = SQLAlchemyMachineConfigRepository(provider=persistence_provider)
    parser = SvgPathToolsParser(wrapper=svg_wrapper)
    generator = PyGCodeGenerator(wrapper=gcode_wrapper)
    
    geom_service = GeometryService()
    converter = ConvertSVGToGCode(parser, generator, repo, geom_service)
    
    return GCodeController(converter=converter, repo=repo)
