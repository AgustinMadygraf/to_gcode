"""
Path: src/dominio/excepciones.py
"""

class ErrorDeDominio(Exception):
    pass

class ConfiguracionNoEncontradaError(ErrorDeDominio):
    pass

class ReglaDeNegocioVioladaError(ErrorDeDominio):
    pass
