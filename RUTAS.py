import os
import sys

def ruta_absoluta(rel_path):
    """Soporta ejecución como .py o .exe"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, rel_path)
    return os.path.join(os.path.abspath("."), rel_path)