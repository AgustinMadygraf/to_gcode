import pytest
from unittest.mock import MagicMock
from src.domain.entities.geometry import Path, Point
from src.domain.entities.machine_config import MachineConfig
from src.application.use_cases.convert_image import ConvertImageToGCode

def test_convert_image_success():
    # Mocks
    mock_parser = MagicMock()
    mock_generator = MagicMock()
    mock_repo = MagicMock()
    mock_geometry_service = MagicMock()
    mock_transformer = MagicMock()
    mock_pattern_generator = MagicMock()
    
    # Setup
    config = MachineConfig(
        name="test", width=100.0, height=100.0,
        max_x=100.0, max_y=100.0,
        pen_up_command="M5", pen_down_command="M3",
        feedrate_draw=10.0, feedrate_move=10.0
    )
    mock_repo.get_config.return_value = config
    
    raw_paths = [Path(points=[Point(x=0, y=0), Point(x=10, y=10)])]
    mock_parser.parse_image.return_value = raw_paths
    mock_transformer.fit_and_orient.return_value = (raw_paths, "landscape")
    mock_generator.generate.return_value = "G0 X0 Y0"
    
    # Execution
    use_case = ConvertImageToGCode(mock_parser, mock_generator, mock_repo, mock_geometry_service, mock_transformer, mock_pattern_generator)
    result = use_case.execute(b"dummy_image_data")
    
    # Assertions
    mock_repo.get_config.assert_called_once()
    mock_parser.parse_image.assert_called_once()
    mock_generator.generate.assert_called_once()
    assert result == "G0 X0 Y0"
