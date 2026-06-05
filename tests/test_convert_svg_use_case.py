import pytest
from unittest.mock import MagicMock
from src.application.use_cases.convert_svg import ConvertSVGToGCode
from src.domain.entities.machine_config import MachineConfig
from src.domain.entities.geometry import Path, Point

def test_convert_svg_success():
    # Mocks
    mock_parser = MagicMock()
    mock_generator = MagicMock()
    mock_repo = MagicMock()
    mock_geometry_service = MagicMock()
    mock_transformer = MagicMock()
    mock_pattern_generator = MagicMock()
    mock_optimizer = MagicMock()

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
    mock_optimizer.optimize.return_value = raw_paths
    mock_generator.generate.return_value = "G0 X0 Y0"

    # Execution
    use_case = ConvertSVGToGCode(
        mock_parser, 
        mock_generator, 
        mock_repo, 
        mock_geometry_service, 
        mock_transformer, 
        mock_pattern_generator,
        mock_optimizer
    )
    result = use_case.execute(svg_content)

    # Assertions
    assert result == "G0 X0 Y0"
    mock_optimizer.optimize.assert_called_once()

def test_convert_svg_no_config():
    # Setup
    mock_repo = MagicMock()
    mock_repo.get_config.return_value = None
    mock_geometry_service = MagicMock()
    mock_transformer = MagicMock()
    mock_pattern_generator = MagicMock()
    mock_optimizer = MagicMock()

    use_case = ConvertSVGToGCode(
        MagicMock(), 
        MagicMock(), 
        mock_repo, 
        mock_geometry_service, 
        mock_transformer, 
        mock_pattern_generator,
        mock_optimizer
    )
    
    with pytest.raises(ValueError, match="Machine configuration not found"):
        use_case.execute("<svg/>")
