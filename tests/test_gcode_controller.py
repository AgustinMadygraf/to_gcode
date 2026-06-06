import pytest
from unittest.mock import MagicMock
from src.adaptadores.controladores.controlador_codigo_g import ControladorCodigoG
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina

@pytest.fixture
def mock_svg_converter():
    return MagicMock()

@pytest.fixture
def mock_image_converter():
    return MagicMock()

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def controller(mock_svg_converter, mock_image_converter, mock_repo):
    return ControladorCodigoG(
        svg_converter=mock_svg_converter, 
        image_converter=mock_image_converter, 
        repo=mock_repo
    )

def test_set_config(controller, mock_repo):
    # Ahora el controlador recibe datos ya normalizados por la infraestructura
    config_data = {
        "name": "test", "ancho": 100.0, "alto": 100.0,
        "max_x": 100.0, "max_y": 100.0,
        "pen_up_command": "M5", "pen_down_command": "M3",
        "velocidad_dibujo": 10.0, "velocidad_movimiento": 10.0
    }
    controller.set_config(config_data)
    
    assert mock_repo.save_config.called
    saved_entity = mock_repo.save_config.call_args[0][0]
    assert isinstance(saved_entity, ConfiguracionMaquina)
    assert saved_entity.name == "test"

def test_get_config_not_found(controller, mock_repo):
    mock_repo.get_config.return_value = None
    result = controller.get_config()
    assert result is None

def test_get_config_found(controller, mock_repo):
    config = ConfiguracionMaquina(
        nombre="test", ancho=100.0, alto=100.0,
        ancho_maximo_maquina=100.0, alto_maximo_maquina=100.0,
        comando_pluma_arriba="M5", comando_pluma_abajo="M3",
        velocidad_dibujo=10.0, velocidad_movimiento=10.0
    )
    mock_repo.get_config.return_value = config
    
    result = controller.get_config()
    # Validar que el Presenter estructuró la salida correctamente
    assert result["name"] == "test"
    assert result["dimensions"]["ancho"] == 100.0
    assert result["limits"]["max_x"] == 100.0
    assert result["speeds"]["draw"] == 10.0

def test_convertir_svg(controller, mock_svg_converter):
    mock_svg_converter.execute.return_value = "G0 X0 Y0"
    result = controller.convertir_svg("<svg>...</svg>")
    
    mock_svg_converter.execute.assert_called_once()
    assert result["gcode"] == "G0 X0 Y0"
