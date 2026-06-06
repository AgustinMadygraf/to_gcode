"""
Path: src/dominio/entidades/geometria.py
"""

from dataclasses import dataclass
from typing import List, Optional
from abc import ABC, abstractmethod
import math

@dataclass(frozen=True)
class Punto:
    x: float
    y: float

    def distancia_a(self, otro: 'Punto') -> float:
        return math.sqrt((self.x - otro.x)**2 + (self.y - otro.y)**2)

@dataclass(frozen=True)
class Arco:
    centro: Punto
    radio: float
    punto_inicio: Punto
    punto_fin: Punto
    es_horario: bool = True

class Segmento(ABC):
    @property
    @abstractmethod
    def inicio(self) -> Punto: pass
    
    @property
    @abstractmethod
    def fin(self) -> Punto: pass

@dataclass(frozen=True)
class SegmentoLinea(Segmento):
    p1: Punto
    p2: Punto
    
    @property
    def inicio(self) -> Punto: return self.p1
    
    @property
    def fin(self) -> Punto: return self.p2

@dataclass(frozen=True)
class SegmentoArco(Segmento):
    arco: Arco
    
    @property
    def inicio(self) -> Punto: return self.arco.punto_inicio
    
    @property
    def fin(self) -> Punto: return self.arco.punto_fin

@dataclass(frozen=True)
class Trayectoria:
    puntos: List[Punto]
    segmentos: Optional[List[Segmento]] = None
    info_arco: Optional[Arco] = None

    @property
    def es_vacia(self) -> bool:
        return len(self.puntos) == 0

    @property
    def punto_inicio(self) -> Punto:
        if self.es_vacia:
            raise ValueError("La trayectoria vacía no tiene punto de inicio")
        return self.puntos[0]

    @property
    def punto_fin(self) -> Punto:
        if self.es_vacia:
            raise ValueError("La trayectoria vacía no tiene punto de fin")
        return self.puntos[-1]

    @property
    def distancia_total(self) -> float:
        if len(self.puntos) < 2:
            return 0.0
        dist = 0.0
        for i in range(len(self.puntos) - 1):
            dist += self.puntos[i].distancia_a(self.puntos[i+1])
        return dist

    def simplificada(self, tolerancia: float = 1e-9) -> 'Trayectoria':
        if len(self.puntos) < 3:
            return self
        
        puntos_simplificados = [self.puntos[0]]
        for i in range(1, len(self.puntos) - 1):
            p1, p2, p3 = self.puntos[i-1], self.puntos[i], self.puntos[i+1]
            # Cálculo de área de triángulo (colinealidad)
            area = abs((p2.y - p1.y) * (p3.x - p2.x) - (p2.x - p1.x) * (p3.y - p2.y))
            if area > tolerancia:
                puntos_simplificados.append(p2)
        puntos_simplificados.append(self.puntos[-1])
        return Trayectoria(puntos=puntos_simplificados, segmentos=self.segmentos, info_arco=self.info_arco)

    def invertida(self) -> 'Trayectoria':
        return Trayectoria(puntos=self.puntos[::-1], info_arco=self.info_arco)

@dataclass(frozen=True)
class Rectangulo:
    min_x: float
    min_y: float
    max_x: float
    max_y: float

    @property
    def ancho(self) -> float: return self.max_x - self.min_x
    @property
    def altura(self) -> float: return self.max_y - self.min_y
