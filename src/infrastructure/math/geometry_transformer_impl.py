from typing import List, Tuple
import math
from src.dominio.entidades.geometria import Trayectoria, Punto as DomainPunto
from src.dominio.entidades.geometria import Rectangulo
from src.dominio.interfaces.transformador_geometria import TransformadorGeometria

class ImplementacionTransformadorGeometria(TransformadorGeometria):
    def _get_bounding_box(self, trayectorias: List[Trayectoria]) -> Rectangulo:
        all_points = [p for path in trayectorias for p in path.puntos]
        if not all_points:
            return Rectangulo(min_x=0.0, min_y=0.0, max_x=0.0, max_y=0.0)
        
        min_x = min(p.x for p in all_points)
        max_x = max(p.x for p in all_points)
        min_y = min(p.y for p in all_points)
        max_y = max(p.y for p in all_points)
        return Rectangulo(min_x=min_x, min_y=min_y, max_x=max_x, max_y=max_y)

    def invertir_eje_y(self, trayectorias: List[Trayectoria]) -> List[Trayectoria]:
        box = self._get_bounding_box(trayectorias)
        inverted_trayectorias: List[Trayectoria] = []
        for path in trayectorias:
            new_points = [
                DomainPunto(x=p.x, y=box.max_y - (p.y - box.min_y))
                for p in path.puntos
            ]
            inverted_trayectorias.append(Trayectoria(puntos=new_points))
        return inverted_trayectorias

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

    def _scale_and_translate(self, trayectorias: List[Trayectoria], scale: float, offset: DomainPunto) -> List[Trayectoria]:
        trayectorias_transformadas: List[Trayectoria] = []
        for path in trayectorias:
            new_points = [
                DomainPunto(x=p.x * scale + offset.x, y=p.y * scale + offset.y)
                for p in path.puntos
            ]
            trayectorias_transformadas.append(Trayectoria(puntos=new_points))
        return trayectorias_transformadas

    def ajustar_y_orientar(self, trayectorias: List[Trayectoria], limites_paisaje: Rectangulo, limites_retrato: Rectangulo) -> Tuple[List[Trayectoria], str]:
        drawing_box = self._get_bounding_box(trayectorias)
        
        scale_l = min(limites_paisaje.ancho / drawing_box.ancho, limites_paisaje.altura / drawing_box.altura)
        scale_p = min(limites_retrato.ancho / drawing_box.ancho, limites_retrato.altura / drawing_box.altura)
        
        if scale_p > scale_l:
            best_scale = scale_p
            orientation = "portrait"
            trayectorias = [self._rotate_path(p, 90) for p in trayectorias]
            final_drawing_box = self._get_bounding_box(trayectorias)
            target_box = limites_retrato
        else:
            best_scale = scale_l
            orientation = "landscape"
            final_drawing_box = drawing_box
            target_box = limites_paisaje
            
        ancho_dibujo_escalado = final_drawing_box.ancho * best_scale
        alto_dibujo_escalado = final_drawing_box.altura * best_scale
        
        margen_x = (target_box.ancho - ancho_dibujo_escalado) / 2
        margen_y = (target_box.altura - alto_dibujo_escalado) / 2
        
        offset = DomainPunto(
            x=target_box.min_x - final_drawing_box.min_x * best_scale + margen_x,
            y=target_box.min_y - final_drawing_box.min_y * best_scale + margen_y
        )
        
        trayectorias_transformadas = self._scale_and_translate(trayectorias, best_scale, offset)
        
        return trayectorias_transformadas, orientation
