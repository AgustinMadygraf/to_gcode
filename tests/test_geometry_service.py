import pytest
from src.domain.entities.machine_config import MachineConfig, Path, Point
from src.domain.services.geometry_service import GeometryService

@pytest.fixture
def config():
    return MachineConfig(
        name="test_machine",
        width=100.0,
        height=100.0,
        pen_up_command="M5",
        pen_down_command="M3",
        feedrate_draw=1000.0,
        feedrate_move=2000.0,
        invert_y=True,
        scale_to_fit=False
    )

@pytest.fixture
def geometry_service():
    return GeometryService()

def test_transform_no_scale_no_invert():
    # Setup: disable invert_y for simpler test
    cfg = MachineConfig(
        name="cfg", width=100.0, height=100.0, 
        pen_up_command="M5", pen_down_command="M3",
        feedrate_draw=10.0, feedrate_move=10.0,
        invert_y=False, scale_to_fit=False
    )
    service = GeometryService()
    path = Path(points=[Point(x=10.0, y=20.0)])
    
    transformed = service.transform_paths([path], cfg)
    
    assert transformed[0].points[0].x == 10.0
    assert transformed[0].points[0].y == 20.0

def test_transform_invert_y(config):
    # Setup: config has invert_y=True, height=100
    service = GeometryService()
    path = Path(points=[Point(x=10.0, y=20.0)])
    
    transformed = service.transform_paths([path], config)
    
    # 100 - 20 = 80
    assert transformed[0].points[0].x == 10.0
    assert transformed[0].points[0].y == 80.0

def test_calculate_scale(config):
    # Setup: points are 0..50, machine is 100x100 -> scale should be 2.0
    cfg = MachineConfig(
        name="cfg", width=100.0, height=100.0, 
        pen_up_command="M5", pen_down_command="M3",
        feedrate_draw=10.0, feedrate_move=10.0,
        invert_y=False, scale_to_fit=True
    )
    service = GeometryService()
    path = Path(points=[Point(x=0.0, y=0.0), Point(x=50.0, y=50.0)])
    
    transformed = service.transform_paths([path], cfg)
    
    # 0*2=0, 50*2=100
    assert transformed[0].points[1].x == 100.0
    assert transformed[0].points[1].y == 100.0
