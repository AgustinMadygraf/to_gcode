import pytest
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina

@pytest.fixture
def default_config():
    return ConfiguracionMaquina(
        name="test_machine",
        width=100.0,
        height=100.0,
        max_x=100.0,
        max_y=100.0,
        pen_up_command="M5",
        pen_down_command="M3",
        feedrate_draw=100.0,
        feedrate_move=500.0
    )
