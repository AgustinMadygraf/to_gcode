"""
Trayectoria: src/domain/services/geometry_service.py
"""

from typing import List, Optional
from src.dominio.interfaces.procesador_geometria import ProcesadorGeometria
from src.dominio.entidades.geometria import Punto, Arco, Trayectoria

class ServicioGeometria:
    """Servicio de dominio para operaciones geométricas complejas."""
    
    def __init__(self, procesador_geometria: ProcesadorGeometria):
        self.procesador = procesador_geometria

    def ajustar_arco(self, puntos: List[Punto], tolerancia: float) -> Optional[Arco]:
        """
        Intenta ajustar un arco circular a una secuencia de punsrc.dominio.servicestos.
        Retorna un objeto Arco si el ajuste está dentro de la tolerancia.
        """
        if len(puntos) < 3:
            return None
            
        p1, p2, p3 = puntos[0], puntos[len(puntos)//2], puntos[-1]
        circle = self.procesador.obtener_circulo_desde_tres_puntos(p1, p2, p3)
        if not circle:
            return None
            
        centro, radio = circle
        max_dev, _ = self.procesador.calcular_maxima_desviacion(puntos, centro, radio)
        
        if max_dev <= tolerancia:
            return Arco(
                centro=centro,
                radio=radio,
                punto_inicio=puntos[0],
                punto_fin=puntos[-1]
            )
        
        return None

    def simplificar_trayectoria_a_arcos(self, trayectoria: Trayectoria, tolerancia: float) -> List[Trayectoria]:
        """
        Divide una trayectoria en segmentos de líneas o arcos.
        (Lógica simplificada para ilustración del uso del nuevo VO Arco)
        """
        arco = self.ajustar_arco(trayectoria.puntos, tolerancia)
        if arco:
            # Retornamos el mismo trayectoria pero enriquecido con info de arco
            return [Trayectoria(puntos=trayectoria.puntos, info_arco=arco)]
        return [trayectoria]
