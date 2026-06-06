"""
Trayectoria: src/infrastructure/math/geometry_transformer_impl.py
"""

from typing import List, Tuple
import math
from src.dominio.entidades.geometria import Trayectoria, Punto as DomainPunto
from src.dominio.entidades.geometria import Rectangulo
from src.dominio.interfaces.transformador_geometria import TransformadorGeometria

class ImplementacionTransformadorGeometria(TransformadorGeometria):
    def _get_bounding_box(self, paths: List[Trayectoria]) -> Rectangulo:
        all_points = [p for path in paths for p in path.puntos]
        if not all_points:
            return Rectangulo(0.0, 0.0, 0.0, 0.0)
        
        min_x = min(p.x for p in all_points)
        max_x = max(p.x for p in all_points)
        min_y = min(p.y for p in all_points)
        max_y = max(p.y for p in all_points)
        return Rectangulo(min_x, min_y, max_x, max_y)

    def _rotate_path(self, path: Trayectoria, angle_deg: float) -> Trayectoria:
        angle_rad = math.radians(angle_deg)
        new_points: List[DomainPunto] = []
        for p in path.puntos:
            new_x = p.x * math.cos(angle_rad) - p.y * math.sin(angle_rad)
            new_y = p.x * math.sin(angle_rad) + p.y * math.cos(angle_rad)
            new_points.append(DomainPunto(x=new_x, y=new_y))
        
        min_x = min(p.x for p in new_points)
        min_y = min(p.y for p in new_points)
        normalized_points = [DomainPunto(x=p.x - min_x, y=p.y - min_y) for p in new_points]
        
        return Trayectoria(puntos=normalized_points)

    def _scale_and_translate(self, paths: List[Trayectoria], scale: float, offset: DomainPunto) -> List[Trayectoria]:
        transformed_paths: List[Trayectoria] = []
        for path in paths:
            new_points = [
                DomainPunto(x=p.x * scale + offset.x, y=p.y * scale + offset.y)
                for p in path.puntos
            ]
            transformed_paths.append(Trayectoria(puntos=new_points))
        return transformed_paths

    def fit_and_orient(self, paths: List[Trayectoria], landscape_limits: Rectangulo, portrait_limits: Rectangulo) -> Tuple[List[Trayectoria], str]:
        drawing_box = self._get_bounding_box(paths)
        
        scale_l = min(landscape_limits.ancho / drawing_box.ancho, landscape_limits.altura / drawing_box.altura)
        scale_p = min(portrait_limits.ancho / drawing_box.ancho, portrait_limits.altura / drawing_box.altura)
        
        if scale_p > scale_l:
            best_scale = scale_p
            orientation = "portrait"
            paths = [self._rotate_path(p, 90) for p in paths]
            final_drawing_box = self._get_bounding_box(paths)
            target_box = portrait_limits
        else:
            best_scale = scale_l
            orientation = "landscape"
            final_drawing_box = drawing_box
            target_box = landscape_limits
            
        offset = DomainPunto(x=target_box.min_x - final_drawing_box.min_x * best_scale, 
                             y=target_box.min_y - final_drawing_box.min_y * best_scale)
        
        transformed_paths = self._scale_and_translate(paths, best_scale, offset)
        
        return transformed_paths, orientation
