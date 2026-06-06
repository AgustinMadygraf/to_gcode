"""
Path: src/adaptadores/pasarelas/analizador_vectorial.py
"""

from typing import List
from src.aplicacion.limites.puertos import AnalizadorVectorial
from src.adaptadores.pasarelas.envoltorios_tecnicos import EnvoltorioLibreriaSvg
from src.dominio.entidades.geometria import Trayectoria as TrayectoriaDominio

class AnalizadorSvgToolsTrayectoria(AnalizadorVectorial):
    def __init__(self, envoltorio: EnvoltorioLibreriaSvg, resolucion_muestreo: int = 50):
        self.envoltorio = envoltorio
        self.resolucion_muestreo = resolucion_muestreo

    def parsear_svg(self, contenido_svg: str) -> List[TrayectoriaDominio]:
        try:
            trayectorias = self.envoltorio.obtener_trayectorias_desde_str(contenido_svg)
        except Exception as e:
            raise ValueError(f"Error al analizar SVG: {str(e)}")
        
        trayectorias_dominio: List[TrayectoriaDominio] = []
        for trayectoria in trayectorias:
            # El adaptador ya no sabe que existen números complejos
            puntos = self.envoltorio.muestrear_trayectoria_a_dominio(trayectoria, self.resolucion_muestreo)
            trayectorias_dominio.append(TrayectoriaDominio(puntos=puntos))
        return trayectorias_dominio
