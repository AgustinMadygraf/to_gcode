import pytest
from unittest.mock import MagicMock
from src.adaptadores.controladores.controlador_codigo_g import ControladorCodigoG
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina
from src.aplicacion.dto.solicitudes import ConversionSvgRequest

@pytest.fixture
def mock_svg_converter():
    return MagicMock()

@pytest.fixture
def mock_image_converter():
    return MagicMock()

@pytest.fixture
def mock_gestor_config():
    return MagicMock()

@pytest.fixture
def controller(mock_svg_converter, mock_image_converter, mock_gestor_config):
    return ControladorCodigoG(
        conversor_svg=mock_svg_converter, 
        conversor_imagen=mock_image_converter, 
        gestor_configuracion=mock_gestor_config
    )

def test_convertir_svg(controller, mock_svg_converter):
    mock_svg_converter.ejecutar.return_value = "G0 X0 Y0"
    result = controller.convertir_svg("<svg>...</svg>")
    
    # Assert
    mock_svg_converter.ejecutar.assert_called_once()
    # Verify the argument passed is an instance of ConversionSvgRequest
    assert isinstance(mock_svg_converter.ejecutar.call_args[0][0], ConversionSvgRequest)
    assert mock_svg_converter.ejecutar.call_args[0][0].contenido_svg == "<svg>...</svg>"
    assert result["gcode"] == "G0 X0 Y0"
