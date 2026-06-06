import pytest
from unittest.mock import MagicMock
from src.adapters.pasarelas.repositorio_configuracion_maquina_impl import RepositorioConfiguracionMaquinaImpl
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina

@pytest.fixture
def mock_provider():
    return MagicMock()

@pytest.fixture
def repo(mock_provider):
    return RepositorioConfiguracionMaquinaImpl(provider=mock_provider)

def test_get_config_calls_provider(repo, mock_provider):
    mock_provider.find_first.return_value = {
        "name": "test", "width": 100.0, "height": 100.0,
        "max_x": 100.0, "max_y": 100.0,
        "pen_up_command": "M5", "pen_down_command": "M3",
        "feedrate_draw": 10.0, "feedrate_move": 10.0,
        "invert_y": True, "scale_to_fit": True
    }
    
    config = repo.get_config()
    
    mock_provider.find_first.assert_called_once()
    assert config.name == "test"
    assert config.max_x == 100.0

def test_save_config_calls_provider(repo, mock_provider):
    config = ConfiguracionMaquina(
        name="test", width=100.0, height=100.0,
        max_x=100.0, max_y=100.0,
        pen_up_command="M5", pen_down_command="M3",
        feedrate_draw=10.0, feedrate_move=10.0
    )
    repo.save_config(config)
    
    assert mock_provider.upsert.called
    args = mock_provider.upsert.call_args[0]
    assert args[0] == "test"
    assert args[1]["width"] == 100.0
    assert args[1]["max_x"] == 100.0
