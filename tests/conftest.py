import pytest
from src.dominio.entidades.configuracion_maquina import ConfiguracionMaquina

@pytest.fixture
def default_config():
    return ConfiguracionMaquina(
        name="test_machine",
        ancho=100.0,
        alto=100.0,
        ancho_maximo_maquina=100.0,
        alto_maximo_maquina=100.0,
        comando_pluma_arriba="M5",
        comando_pluma_abajo="M3",
        velocidad_dibujo=100.0,
        velocidad_movimiento=500.0
    )
