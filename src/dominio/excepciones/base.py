"""
Path: src/dominio/excepciones.py

"""

class ErrorDeDominio(Exception):
    """Excepción base para todos los errores de negocio."""
    pass

class ConfiguracionNoEncontradaError(ErrorDeDominio):
    """Lanzado cuando no se encuentra la configuración necesaria."""
    pass

class ReglaDeNegocioVioladaError(ErrorDeDominio):
    """Lanzado cuando se viola una invariante de dominio."""
    pass
