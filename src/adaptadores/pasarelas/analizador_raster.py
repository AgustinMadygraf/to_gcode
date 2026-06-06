"""
Path: src/adaptadores/pasarelas/analizador_raster.py
"""

from typing import List, Set, Tuple
from src.dominio.entidades.geometria import Trayectoria as TrayectoriaDominio, Punto
from src.adaptadores.pasarelas.envoltorios_tecnicos import AbstraccionEsqueleto, ProcesadorImagenRaster
from src.aplicacion.limites.puertos import AnalizadorRaster as AnalizadorRasterBoundary

class AnalizadorRaster(AnalizadorRasterBoundary):
    def __init__(self, procesador: ProcesadorImagenRaster):
        self.procesador = procesador

    def parsear_imagen(self, bytes_imagen: bytes) -> List[TrayectoriaDominio]:
        esqueleto: AbstraccionEsqueleto = self.procesador.procesar_imagen_a_esqueleto(bytes_imagen)
        return self._trazar_esqueleto(esqueleto)

    def _trazar_esqueleto(self, esqueleto: AbstraccionEsqueleto) -> List[TrayectoriaDominio]:
        trayectorias: List[TrayectoriaDominio] = []
        visitados: Set[Tuple[int, int]] = set()
        filas: int = esqueleto.filas
        columnas: int = esqueleto.columnas

        for f in range(filas):
            for c in range(columnas):
                if esqueleto.esta_pixel_encendido(c, f) and (f, c) not in visitados:
                    puntos_trayectoria: List[Tuple[int, int]] = []
                    # Usar enfoque iterativo para evitar RecursionError
                    pila: List[Tuple[int, int]] = [(f, c)]
                    while pila:
                        f_actual, c_actual = pila.pop()
                        if (f_actual, c_actual) in visitados:
                            continue
                            
                        visitados.add((f_actual, c_actual))
                        puntos_trayectoria.append((f_actual, c_actual))
                        
                        for df in [-1, 0, 1]:
                            for dc in [-1, 0, 1]:
                                if df == 0 and dc == 0:
                                    continue
                                nf, nc = f_actual + df, c_actual + dc
                                if 0 <= nf < filas and 0 <= nc < columnas:
                                    if esqueleto.esta_pixel_encendido(nc, nf) and (nf, nc) not in visitados:
                                        pila.append((nf, nc))
                                        
                    if len(puntos_trayectoria) > 1:
                        trayectorias.append(TrayectoriaDominio(puntos=[Punto(x=float(c), y=float(filas - f)) for f, c in puntos_trayectoria]))
        return trayectorias
