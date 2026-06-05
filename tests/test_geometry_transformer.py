import pytest
from src.domain.entities.machine_config import Path, Point as DomainPoint
from src.domain.entities.geometry import Rect
from src.infrastructure.math.geometry_transformer_impl import GeometryTransformerImpl

def test_geometry_transformer_auto_rotates():
    path = Path(points=[
        DomainPoint(0.0, 0.0),
        DomainPoint(20.0, 0.0),
        DomainPoint(20.0, 10.0),
        DomainPoint(0.0, 10.0)
    ])
    
    transformer = GeometryTransformerImpl()
    landscape_limits = Rect(0.0, 0.0, 100.0, 50.0)
    portrait_limits = Rect(0.0, 0.0, 50.0, 100.0)
    
    transformed_paths, orientation = transformer.fit_and_orient(
        [path], landscape_limits, portrait_limits
    )
    
    assert orientation == "landscape"
    final_box = transformer._get_bounding_box(transformed_paths)
    assert final_box.width == pytest.approx(100.0)
    assert final_box.height == pytest.approx(50.0)

def test_geometry_transformer_chooses_portrait():
    path = Path(points=[
        DomainPoint(0.0, 0.0),
        DomainPoint(10.0, 0.0),
        DomainPoint(10.0, 20.0),
        DomainPoint(0.0, 20.0)
    ])
    
    transformer = GeometryTransformerImpl()
    landscape_limits = Rect(0.0, 0.0, 100.0, 50.0)
    portrait_limits = Rect(0.0, 0.0, 50.0, 100.0)
    
    transformed_paths, orientation = transformer.fit_and_orient(
        [path], landscape_limits, portrait_limits
    )
    
    assert orientation == "portrait"
    
    final_box = transformer._get_bounding_box(transformed_paths)
    assert final_box.width == pytest.approx(100.0)
    assert final_box.height == pytest.approx(50.0)
