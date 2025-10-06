"""
Punto de entrada principal de la aplicación TLV 4.0.

Este módulo inicializa y ejecuta la aplicación de gestión de enlaces.
Puede ejecutarse como módulo principal o importado desde otros scripts.
"""
import sys
import os

# Agregar el directorio padre al path para importaciones absolutas
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Intentar importación relativa (para ejecución como módulo)
    from .ui_main import ejecutar_aplicacion
except ImportError:
    # Importación absoluta (para PyInstaller y ejecución directa)
    from ui_main import ejecutar_aplicacion


def main() -> int:
    """
    Función principal de la aplicación.
    
    Returns:
        Código de salida de la aplicación (0 = éxito, 1 = error)
    """
    return ejecutar_aplicacion()


if __name__ == "__main__":
    # Ejecutar aplicación si se llama directamente
    sys.exit(main())