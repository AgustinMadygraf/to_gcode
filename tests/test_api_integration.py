import pytest
import os
from fastapi.testclient import TestClient
from src.infrastructure.fastapi.app import app
from src.infrastructure.database.models import init_db, Base, engine

# Usar DB en memoria para tests aislados
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # Limpiar tablas antes de cada test
    Base.metadata.drop_all(bind=engine)
    init_db()

def test_convert_endpoint_success():
    # Pre-configurar máquina necesaria para el use case
    config_data = {
        "name": "test_plotter",
        "width": 100.0,
        "height": 100.0,
        "pen_up_command": "M5",
        "pen_down_command": "M3",
        "feedrate_draw": 1000.0,
        "feedrate_move": 2000.0
    }
    client.post("/config", json=config_data)
    
    # Ejecutar conversión
    svg_content = "<svg viewBox='0 0 100 100'><path d='M0 0 L10 10'/></svg>"
    files = {"file": ("test.svg", svg_content, "image/svg+xml")}
    
    response = client.post("/convert", files=files)
    
    assert response.status_code == 200
    assert "gcode" in response.json()

def test_convert_without_config():
    # Sin configurar la máquina, debería fallar
    svg_content = "<svg>...</svg>"
    files = {"file": ("test.svg", svg_content, "image/svg+xml")}
    
    response = client.post("/convert", files=files)
    # Debería retornar 400 (config not found)
    assert response.status_code == 400

def test_convert_invalid_svg():
    # Pre-configurar máquina necesaria
    config_data = {
        "name": "test_plotter",
        "width": 100.0,
        "height": 100.0,
        "pen_up_command": "M5",
        "pen_down_command": "M3",
        "feedrate_draw": 1000.0,
        "feedrate_move": 2000.0
    }
    client.post("/config", json=config_data)
    
    # SVG inválido (ej. contenido basura)
    svg_content = "NOT_AN_SVG"
    files = {"file": ("test.svg", svg_content, "image/svg+xml")}
    
    # Debería fallar con 400 ya que el parser fallará
    response = client.post("/convert", files=files)
    assert response.status_code == 400

def test_config_lifecycle():
    # Test POST /config
    config_data = {
        "name": "production_plotter",
        "width": 200.0,
        "height": 200.0,
        "pen_up_command": "M5",
        "pen_down_command": "M3",
        "feedrate_draw": 500.0,
        "feedrate_move": 1000.0
    }
    response = client.post("/config", json=config_data)
    assert response.status_code == 201
    
    # Test GET /config
    response = client.get("/config")
    assert response.status_code == 200
    assert response.json()["name"] == "production_plotter"
