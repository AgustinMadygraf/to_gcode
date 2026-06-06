import pytest
from unittest.mock import MagicMock
from src.adaptadores.pasarelas.repositorio_configuracion_maquina_impl import RepositorioConfiguracionMaquinaImpl
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina

@pytest.fixture
def mock_provider():
    return MagicMock()

@pytest.fixture
def repo(mock_provider):
    return RepositorioConfiguracionMaquinaImpl(provider=mock_provider)

def test_get_config_calls_provider(repo, mock_provider):
    mock_provider.find_first.return_value = {
        "name": "test", "ancho": 100.0, "alto": 100.0,
        "max_x": 100.0, "max_y": 100.0,
        "pen_up_command": "M5", "pen_down_command": "M3",
        "velocidad_dibujo": 10.0, "velocidad_movimiento": 10.0,
        "invertir_y": True, "ajustar_a_escala": True
    }
    
    config = repo.get_config()
    
    mock_provider.find_first.assert_called_once()
    assert config.name == "test"
    assert config.max_x == 100.0

def test_save_config_calls_provider(repo, mock_provider):
    config = ConfiguracionMaquina(
        nombre="test", ancho=100.0, alto=100.0,
        ancho_maximo_maquina=100.0, alto_maximo_maquina=100.0,
        comando_pluma_arriba="M5", comando_pluma_abajo="M3",
        velocidad_dibujo=10.0, velocidad_movimiento=10.0
    )
    repo.save_config(config)
    
    assert mock_provider.upsert.called
    args = mock_provider.upsert.call_args[0]
    assert args[0] == "test"
    assert args[1]["ancho"] == 100.0
    assert args[1]["max_x"] == 100.0
