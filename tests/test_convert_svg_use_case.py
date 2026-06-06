import pytest
from unittest.mock import MagicMock
from src.aplicacion.casos_de_uso.convertir_svg import ConvertirSVGAGCode
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina
from src.dominio.entidades.geometria import Trayectoria, Punto

def test_convertir_svg_success():
    # Mocks
    mock_parser = MagicMock()
    mock_generator = MagicMock()
    mock_repo = MagicMock()
    mock_prep_service = MagicMock()
    mock_optimizer = MagicMock()

    # Setup
    config = ConfiguracionMaquina(
        nombre="test", ancho=100.0, alto=100.0,
        ancho_maximo_maquina=100.0, alto_maximo_maquina=100.0,
        comando_pluma_arriba="M5", comando_pluma_abajo="M3",
        velocidad_dibujo=10.0, velocidad_movimiento=10.0
    )
    mock_repo.get_config.return_value = config

    svg_content = "<svg>...</svg>"
    raw_paths = [Trayectoria(puntos=[Punto(x=0, y=0), Punto(x=10, y=10)])]

    mock_parser.parse_svg.return_value = raw_paths
    mock_prep_service.prepare.return_value = raw_paths
    mock_optimizer.optimize.return_value = raw_paths
    mock_generator.generate.return_value = "G0 X0 Y0"

    # Execution
    use_case = ConvertirSVGAGCode(
        mock_parser, 
        mock_generator, 
        mock_repo, 
        mock_prep_service,
        mock_optimizer
    )
    result = use_case.ejecutar(svg_content)

    # Assertions
    assert result == "G0 X0 Y0"
    mock_prep_service.prepare.assert_called_once()
    mock_optimizer.optimize.assert_called_once()

def test_convertir_svg_no_config():
    # Setup
    mock_repo = MagicMock()
    mock_repo.get_config.return_value = None

    use_case = ConvertirSVGAGCode(
        MagicMock(), 
        MagicMock(), 
        mock_repo, 
        MagicMock(),
        MagicMock()
    )
    
    with pytest.raises(ValueError, match="Machine configuration not found"):
        use_case.ejecutar("<svg/>")
