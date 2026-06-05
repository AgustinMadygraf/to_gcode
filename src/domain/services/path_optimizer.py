from typing import List
from src.domain.entities.geometry import Path
from src.domain.interfaces.path_optimizer import PathOptimizer

class GreedyPathOptimizer(PathOptimizer):
    """
    Implementación voraz (Greedy) del problema del viajante para trayectorias.
    Busca siempre la trayectoria más cercana al punto actual del cabezal.
    """

    def optimize(self, paths: List[Path]) -> List[Path]:
        # Filtrar trayectorias inválidas usando lógica de la entidad
        valid_paths = [p for p in paths if not p.is_empty]
        if not valid_paths:
            return []
        
        # Ordenar inicialmente por distancia total (opcional, heurística simple)
        unvisited = sorted(valid_paths, key=lambda p: p.total_distance, reverse=True)
        
        current_path = unvisited.pop(0)
        optimized = [current_path]
        
        while unvisited:
            # Buscar la trayectoria cuyo punto de inicio esté más cerca del final de la actual
            last_point = current_path.end_point
            
            # Usamos el comportamiento de Point para calcular distancias
            next_path = min(unvisited, key=lambda p: last_point.distance_to(p.start_point))
            
            unvisited.remove(next_path)
            optimized.append(next_path)
            current_path = next_path
            
        return optimized

# Mantener compatibilidad temporal con el nombre antiguo si es necesario
PathOptimizerService = GreedyPathOptimizer
