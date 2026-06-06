import pytest
from unittest.mock import MagicMock
from src.application.use_cases.convert_image import ConvertImageToGCode
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina
from src.dominio.entidades.geometria import Trayectoria, Punto

def test_convert_image_success():
    # Mocks
    mock_parser = MagicMock()
    mock_generator = MagicMock()
    mock_repo = MagicMock()
    mock_prep_service = MagicMock()
    mock_optimizer = MagicMock()

    # Setup
    config = ConfiguracionMaquina(
        name="test", width=100.0, height=100.0,
        max_x=100.0, max_y=100.0,
        pen_up_command="M5", pen_down_command="M3",
        feedrate_draw=10.0, feedrate_move=10.0
    )
    mock_repo.get_config.return_value = config

    raw_paths = [Trayectoria(points=[Punto(x=0, y=0), Punto(x=10, y=10)])]
    mock_parser.parse_image.return_value = raw_paths
    mock_prep_service.prepare.return_value = raw_paths
    mock_optimizer.optimize.return_value = raw_paths
    mock_generator.generate.return_value = "G0 X0 Y0"

    # Execution
    use_case = ConvertImageToGCode(
        mock_parser, 
        mock_generator, 
        mock_repo, 
        mock_prep_service,
        mock_optimizer
    )
    result = use_case.execute(b"fake_image_bytes")

    # Assertions
    assert result == "G0 X0 Y0"
    mock_prep_service.prepare.assert_called_once()
    mock_optimizer.optimize.assert_called_once()
