#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRUEBA SISTEMA DE FAVORITOS - TECH LINK VIEWER 4.0
Script para probar todas las funcionalidades del sistema de favoritos
"""

import sys
import os

# Agregar el directorio raíz del proyecto al path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from app.views.main_window import VentanaPrincipal
from pathlib import Path

def crear_datos_prueba():
    """Crea algunos enlaces de prueba con favoritos"""
    print("🧪 PRUEBA DEL SISTEMA DE FAVORITOS")
    print("="*60)
    print("🎯 Funcionalidades a probar:")
    print("   ⭐ Columna de favoritos en tabla")
    print("   ⭐ Panel lateral de favoritos")
    print("   ⭐ Botón favorito en toolbar")
    print("   ⭐ Atajos de teclado:")
    print("     - Ctrl+B: Alternar favorito")
    print("     - Ctrl+Shift+B: Mostrar solo favoritos")
    print("   ⭐ Toasts de feedback")
    print("   ⭐ Persistencia automática")
    print()
    print("🔧 INSTRUCCIONES DE PRUEBA:")
    print("1. Observa la nueva columna ⭐ en la tabla")
    print("2. Selecciona un enlace y presiona Ctrl+B")
    print("3. Verifica que aparece en el panel lateral")
    print("4. Haz clic en el botón ⭐ de la toolbar")
    print("5. Usa Ctrl+Shift+B para ver solo favoritos")
    print("6. Haz clic en enlaces del panel lateral")
    print("7. Prueba eliminar favoritos desde el panel")
    print()
    print("✅ DATOS DE PRUEBA:")
    print("   - Google (ya marcado como favorito)")
    print("   - Otros enlaces sin marcar")
    print()

def main():
    """Función principal de prueba"""
    crear_datos_prueba()
    
    # Crear aplicación
    app = QApplication(sys.argv)
    
    # Configurar aplicación
    app.setApplicationName("TECH LINK VIEWER - Prueba Favoritos")
    app.setApplicationVersion("4.0")
    
    # Crear ruta de datos de prueba
    ruta_datos = Path("data/links.json")
    
    # Crear y mostrar ventana principal
    ventana = VentanaPrincipal(ruta_datos)
    ventana.show()
    
    # Timer para mostrar mensaje después de cargar
    def mostrar_ayuda_favoritos():
        if hasattr(ventana, 'repositorio') and hasattr(ventana, 'widget_favoritos'):
            # Contar favoritos existentes
            total_favoritos = ventana.repositorio.contar_favoritos()
            print(f"📊 ESTADO INICIAL: {total_favoritos} favoritos encontrados")
            
            if total_favoritos > 0:
                print("✅ Panel de favoritos debería mostrar enlaces")
                print("✅ Columna ⭐ debería mostrar estrellas llenas")
            else:
                print("ℹ️  Marca algunos enlaces como favoritos para probar")
            
            # Mostrar toast informativo
            from app.widgets.toast_notification import show_info_toast
            show_info_toast("🎯 ¡Prueba el sistema de favoritos! Usa Ctrl+B", duration=5000)
    
    # Ejecutar después de 2 segundos
    QTimer.singleShot(2000, mostrar_ayuda_favoritos)
    
    print("🚀 APLICACIÓN INICIADA - ¡Prueba el sistema de favoritos!")
    print("❌ Para salir: Cierra la ventana o Ctrl+C en terminal")
    print("="*60)
    
    # Ejecutar aplicación
    sys.exit(app.exec())

if __name__ == "__main__":
    main()