import pytest
from unittest.mock import MagicMock
from src.domain.entities.geometry import Path, Point
from src.domain.entities.machine_config import MachineConfig
from src.application.use_cases.convert_svg import ConvertSVGToGCode

def test_convert_svg_success():
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
    
    svg_content = "<svg>...</svg>"
    raw_paths = [Path(points=[Point(x=0, y=0), Point(x=10, y=10)])]
    
    mock_parser.parse_svg.return_value = raw_paths
    mock_transformer.fit_and_orient.return_value = (raw_paths, "landscape")
    mock_generator.generate.return_value = "G0 X0 Y0"
    
    # Execution
    use_case = ConvertSVGToGCode(mock_parser, mock_generator, mock_repo, mock_geometry_service, mock_transformer, mock_pattern_generator)
    result = use_case.execute(svg_content)
    
    # Assertions
    mock_repo.get_config.assert_called_once()
    mock_parser.parse_svg.assert_called_once_with(svg_content)
    mock_generator.generate.assert_called_once()
    assert result == "G0 X0 Y0"

def test_convert_svg_no_config():
    # Setup
    mock_repo = MagicMock()
    mock_repo.get_config.return_value = None
    mock_geometry_service = MagicMock()
    mock_transformer = MagicMock()
    mock_pattern_generator = MagicMock()
    
    use_case = ConvertSVGToGCode(MagicMock(), MagicMock(), mock_repo, mock_geometry_service, mock_transformer, mock_pattern_generator)
    
    # Execution & Assertion
    with pytest.raises(ValueError, match="Machine configuration not found"):
        use_case.execute("<svg>...</svg>")
