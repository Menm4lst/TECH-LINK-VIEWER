#!/usr/bin/env python3
"""
Punto de entrada para la aplicación compilada TLV 4.0.

Este archivo resuelve los problemas de importaciones relativas para PyInstaller.
"""
import sys
import os

def main():
    """
    Función principal de la aplicación compilada.
    
    Configura el entorno y ejecuta la aplicación principal.
    """
    # Obtener el directorio base de la aplicación
    if getattr(sys, 'frozen', False):
        # Si está compilado con PyInstaller
        application_path = os.path.dirname(sys.executable)
        bundle_dir = sys._MEIPASS
    else:
        # Si se ejecuta desde código fuente
        application_path = os.path.dirname(os.path.abspath(__file__))
        bundle_dir = application_path
    
    # Agregar los directorios necesarios al path
    app_dir = os.path.join(bundle_dir, 'app')
    if os.path.exists(app_dir):
        sys.path.insert(0, app_dir)
    else:
        # Fallback: usar el directorio actual
        sys.path.insert(0, bundle_dir)
    
    # Configurar directorio de trabajo para archivos de datos
    data_dir = os.path.join(application_path, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
    
    # Cambiar al directorio de datos para que los archivos JSON se guarden ahí
    os.chdir(application_path)
    
    try:
        # Importar y ejecutar la aplicación
        from app.ui_main import ejecutar_aplicacion
        return ejecutar_aplicacion()
    except ImportError as e:
        print(f"Error de importación: {e}")
        print("Intentando importación alternativa...")
        
        try:
            # Importación alternativa sin paquete app
            import ui_main
            return ui_main.ejecutar_aplicacion()
        except ImportError as e2:
            print(f"Error crítico: No se puede importar la aplicación: {e2}")
            return 1

if __name__ == "__main__":
    sys.exit(main())