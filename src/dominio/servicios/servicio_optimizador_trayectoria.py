"""
Path: src/dominio/servicios/servicio_optimizador_trayectoria.py
"""

from typing import List
from src.dominio.entidades.geometria import Trayectoria
from src.dominio.interfaces.optimizador_trayectoria import OptimizadorTrayectoria

class OptimizadorTrayectoriaVoraz(OptimizadorTrayectoria):
    """
    Implementación voraz (Greedy) del problema del viajante para trayectorias.
    Busca siempre la trayectoria más cercana al punto actual del cabezal.
    """

    def optimizar(self, trayectorias: List[Trayectoria]) -> List[Trayectoria]:
        # Filtrar trayectorias inválidas usando lógica de la entidad
        valid_trayectorias = [p for p in trayectorias if not p.es_vacia]
        if not valid_trayectorias:
            return []
        
        # Ordenar inicialmente por distancia total (opcional, heurística simple)
        unvisited = sorted(valid_trayectorias, key=lambda p: p.distancia_total, reverse=True)
        
        current_path = unvisited.pop(0)
        optimized = [current_path]
        
        while unvisited:
            # Buscar la trayectoria cuyo punto de inicio esté más cerca del final de la actual
            last_point = current_path.punto_fin
            
            # Usamos el comportamiento de Point para calcular distancias
            next_path = min(unvisited, key=lambda p: last_point.distancia_a(p.punto_inicio))
            
            unvisited.remove(next_path)
            optimized.append(next_path)
            current_path = next_path
            
        return optimized

# Mantener compatibilidad temporal con el nombre antiguo si es necesario
ServicioOptimizadorTrayectoria = OptimizadorTrayectoriaVoraz
