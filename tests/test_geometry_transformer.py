import pytest
from src.dominio.entidades.geometria import Trayectoria, Punto as DomainPunto
from src.dominio.entidades.geometria import Rectangulo
from src.infrastructure.math.geometry_transformer_impl import GeometryTransformerImpl

def test_geometry_transformer_auto_rotates():
    path = Trayectoria(puntos=[
        DomainPunto(x=0.0, y=0.0),
        DomainPunto(x=20.0, y=0.0),
        DomainPunto(x=20.0, y=10.0),
        DomainPunto(x=0.0, y=10.0)
    ])
    
    transformer = GeometryTransformerImpl()
    landscape_limits = Rectangulo(0.0, 0.0, 100.0, 50.0)
    portrait_limits = Rectangulo(0.0, 0.0, 50.0, 100.0)
    
    transformed_paths, orientation = transformer.fit_and_orient(
        [path], landscape_limits, portrait_limits
    )
    
    assert orientation == "landscape"
    final_box = transformer._get_bounding_box(transformed_paths)
    assert final_box.ancho == pytest.approx(100.0)
    assert final_box.altura == pytest.approx(50.0)

def test_geometry_transformer_chooses_portrait():
    path = Trayectoria(puntos=[
        DomainPunto(x=0.0, y=0.0),
        DomainPunto(x=10.0, y=0.0),
        DomainPunto(x=10.0, y=20.0),
        DomainPunto(x=0.0, y=20.0)
    ])
    
    transformer = GeometryTransformerImpl()
    landscape_limits = Rectangulo(0.0, 0.0, 100.0, 50.0)
    portrait_limits = Rectangulo(0.0, 0.0, 50.0, 100.0)
    
    transformed_paths, orientation = transformer.fit_and_orient(
        [path], landscape_limits, portrait_limits
    )
    
    assert orientation == "portrait"
    
    final_box = transformer._get_bounding_box(transformed_paths)
    assert final_box.ancho == pytest.approx(100.0)
    assert final_box.altura == pytest.approx(50.0)
