"""
Path: src/dominio/interfaces/especificaciones_trayectoria.py
"""

from src.dominio.interfaces.especificacion import Especificacion
from src.dominio.entidades.geometria import Trayectoria, Rectangulo

class TrayectoriaNoVacia(Especificacion[Trayectoria]):
    def es_satisfecha_por(self, candidato: Trayectoria) -> bool:
        return not candidato.es_vacia

class TrayectoriaDentroDeLimites(Especificacion[Trayectoria]):
    def __init__(self, limites: Rectangulo):
        self.limites = limites

    def es_satisfecha_por(self, candidato: Trayectoria) -> bool:
        for punto in candidato.puntos:
            if not (self.limites.min_x <= punto.x <= self.limites.max_x and
                    self.limites.min_y <= punto.y <= self.limites.max_y):
                return False
        return True
