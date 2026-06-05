import pytest
import math
from src.domain.services.geometry_service import GeometryService
from src.infrastructure.math.geometry_wrapper import GeometryWrapper
from src.domain.entities.geometry import Point, Arc

def test_get_circle_from_three_points():
    p1 = Point(x=0.0, y=1.0)
    p2 = Point(x=1.0, y=0.0)
    p3 = Point(x=0.0, y=-1.0)
    
    # Circle with center (0,0) and radius 1
    wrapper = GeometryWrapper()
    result = wrapper.get_circle_from_three_points(p1, p2, p3)
    
    assert result is not None
    center, radius = result
    assert math.isclose(center.x, 0.0, abs_tol=1e-7)
    assert math.isclose(center.y, 0.0, abs_tol=1e-7)
    assert math.isclose(radius, 1.0, abs_tol=1e-7)

def test_fit_arc_simple_circle():
    # Create points along a circle arc
    points = []
    for i in range(11):
        angle = i * (math.pi / 20)  # 0 to 90 degrees
        points.append(Point(x=math.cos(angle), y=math.sin(angle)))
        
    # Inject wrapper into service
    wrapper = GeometryWrapper()
    service = GeometryService(geometry_processor=wrapper)
    
    # Tolerance 0.01
    arc = service.fit_arc(points, 0.01)
    
    assert arc is not None
    assert isinstance(arc, Arc)
    assert math.isclose(arc.radius, 1.0, abs_tol=0.05)
    assert isinstance(arc.center, Point)
