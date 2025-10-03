"""
Interfaz principal de la aplicación - configuración y inicialización.
"""
import sys
import logging
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPalette, QColor
from .views.main_window import VentanaPrincipal
from .theme import apply_dark_theme


def configurar_logging() -> None:
    """Configura el sistema de logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def configurar_aplicacion(app: QApplication) -> None:
    """Configura la aplicación PyQt6."""
    app.setApplicationName("TECH LINK VIEWER")
    app.setApplicationVersion("4.0.0")
    app.setOrganizationName("Tech Link Solutions")
    app.setOrganizationDomain("techlink.dev")
    
    # Aplicar tema oscuro terminal
    apply_dark_theme(app)
    
    # Configurar estilo base
    app.setStyle('Fusion')


def obtener_ruta_datos() -> Path:
    """Obtiene la ruta del archivo de datos."""
    # Obtener directorio de la aplicación
    if getattr(sys, 'frozen', False):
        # Si la aplicación está empaquetada
        app_dir = Path(sys.executable).parent
    else:
        # Si se ejecuta desde código fuente
        app_dir = Path(__file__).parent.parent
    
    data_dir = app_dir / "data"
    data_dir.mkdir(exist_ok=True)
    
    return data_dir / "links.json"


def crear_aplicacion() -> QApplication:
    """Crea y configura la aplicación."""
    # Crear aplicación
    app = QApplication(sys.argv)
    
    # Configurar aplicación
    configurar_aplicacion(app)
    
    return app


def ejecutar_aplicacion() -> int:
    """Ejecuta la aplicación principal."""
    # Configurar logging
    configurar_logging()
    
    logger = logging.getLogger(__name__)
    logger.info("Iniciando aplicación TLV 4.0")
    
    try:
        # Crear aplicación
        app = crear_aplicacion()
        
        # Obtener ruta de datos
        ruta_datos = obtener_ruta_datos()
        logger.info(f"Usando archivo de datos: {ruta_datos}")
        
        # Crear ventana principal
        ventana = VentanaPrincipal(ruta_datos)
        ventana.show()
        
        logger.info("Aplicación iniciada correctamente")
        
        # Ejecutar loop principal
        return app.exec()
        
    except Exception as e:
        logger.error(f"Error fatal: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(ejecutar_aplicacion())