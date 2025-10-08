#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar las correcciones del sistema de toasts
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import QTimer

# Agregar el directorio de la aplicación al path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.widgets import (
    init_toast_system, show_success_toast, show_error_toast,
    show_warning_toast, show_info_toast
)
from app.config import obtener_fluent_colors


class TestWindow(QMainWindow):
    """Ventana de prueba para verificar toasts."""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
        # Inicializar sistema de toasts
        init_toast_system(self)
        
        # Auto-test después de 1 segundo
        QTimer.singleShot(1000, self.run_auto_test)
    
    def setup_ui(self):
        """Configura la interfaz."""
        self.setWindowTitle("🧪 Test de Toasts Corregidos")
        self.setGeometry(100, 100, 800, 600)  # Ventana más grande para mejor testing
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout(central_widget)
        
        # Aplicar estilo Fluent
        colors = obtener_fluent_colors()
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {colors['surface_primary']};
                color: {colors['text_primary']};
            }}
            QWidget {{
                background-color: {colors['surface_primary']};
                color: {colors['text_primary']};
            }}
            QPushButton {{
                background-color: {colors['primary']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                margin: 5px;
            }}
            QPushButton:hover {{
                background-color: {colors['primary_light']};
            }}
        """)
        
        # Botón de prueba manual
        test_button = QPushButton("🔔 Probar Toast Manual")
        test_button.clicked.connect(self.manual_test)
        layout.addWidget(test_button)
    
    def run_auto_test(self):
        """Ejecuta una prueba automática de diferentes tipos de toast."""
        print("🧪 Iniciando prueba automática de toasts...")
        
        # Secuencia de pruebas con delays
        tests = [
            (0, lambda: show_info_toast("ℹ️ Iniciando pruebas de visibilidad")),
            (1000, lambda: show_success_toast("✅ Toast de éxito - Este mensaje debe verse completo")),
            (2500, lambda: show_error_toast("❌ Error crítico - Mensaje largo para probar el ajuste automático de altura")),
            (4000, lambda: show_warning_toast("⚠️ Advertencia importante que debería mostrarse completamente sin cortarse")),
            (5500, lambda: show_info_toast("📊 Información: El contenido de este toast debe ser completamente visible")),
            (7000, lambda: self.test_multiple_toasts()),
        ]
        
        for delay, test_func in tests:
            QTimer.singleShot(delay, test_func)
    
    def test_multiple_toasts(self):
        """Prueba múltiples toasts para verificar apilado."""
        print("📚 Probando múltiples toasts apilados...")
        
        messages = [
            ("success", "🔗 Enlace 1 creado exitosamente"),
            ("success", "🔗 Enlace 2 agregado correctamente"),
            ("warning", "⚠️ URL duplicada detectada en el sistema"),
            ("info", "ℹ️ Proceso de validación completado"),
            ("success", "🎉 Todas las operaciones finalizadas")
        ]
        
        for i, (toast_type, message) in enumerate(messages):
            QTimer.singleShot(i * 600, lambda t=toast_type, m=message: self.show_toast_by_type(t, m))
    
    def show_toast_by_type(self, toast_type, message):
        """Muestra un toast según su tipo."""
        if toast_type == "success":
            show_success_toast(message)
        elif toast_type == "error":
            show_error_toast(message)
        elif toast_type == "warning":
            show_warning_toast(message)
        else:
            show_info_toast(message)
    
    def manual_test(self):
        """Prueba manual individual."""
        show_info_toast("🧪 Prueba manual ejecutada - ¿Se ve este mensaje completo?")


def main():
    """Función principal."""
    app = QApplication(sys.argv)
    
    # Crear y mostrar ventana
    window = TestWindow()
    window.show()
    
    print("🚀 Ventana de prueba abierta")
    print("📋 Verificar que:")
    print("   ✓ Los toasts aparecen completamente visibles")
    print("   ✓ El contenido no se corta")
    print("   ✓ Se apilan correctamente")
    print("   ✓ Las animaciones son suaves")
    
    # Ejecutar aplicación
    sys.exit(app.exec())


if __name__ == "__main__":
    main()