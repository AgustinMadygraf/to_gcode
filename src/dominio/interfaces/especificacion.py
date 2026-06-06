"""
Path: src/dominio/interfaces/especificacion.py
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")

class Especificacion(ABC, Generic[T]):
    @abstractmethod
    def es_satisfecha_por(self, candidato: T) -> bool:
        pass

    def __and__(self, otra: 'Especificacion[T]') -> 'Especificacion[T]':
        return EspecificacionAnd(self, otra)

class EspecificacionAnd(Especificacion[T]):
    def __init__(self, izquierda: Especificacion[T], derecha: Especificacion[T]):
        self.izquierda = izquierda
        self.derecha = derecha

    def es_satisfecha_por(self, candidato: T) -> bool:
        return self.izquierda.es_satisfecha_por(candidato) and self.derecha.es_satisfecha_por(candidato)
