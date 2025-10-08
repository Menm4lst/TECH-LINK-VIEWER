#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba específica para verificar que el botón de cerrar funciona correctamente
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont

# Agregar el directorio de la aplicación al path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.widgets import (
    init_toast_system, show_success_toast, show_error_toast,
    show_warning_toast, show_info_toast
)
from app.config import obtener_fluent_colors


class CloseButtonTestWindow(QMainWindow):
    """Ventana de prueba específica para el botón de cerrar."""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
        # Inicializar sistema de toasts
        init_toast_system(self)
        
        # Mostrar instrucciones después de 1 segundo
        QTimer.singleShot(1000, self.show_instructions)
    
    def setup_ui(self):
        """Configura la interfaz."""
        self.setWindowTitle("🧪 Prueba del Botón de Cerrar Toasts")
        self.setGeometry(100, 100, 700, 500)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        
        # Título
        title = QLabel("🧪 Prueba del Botón de Cerrar (✕)")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #9D4EDD; padding: 10px;")
        layout.addWidget(title)
        
        # Instrucciones
        instructions = QLabel("""
📋 INSTRUCCIONES:
1. Haz clic en los botones para generar toasts
2. Cada toast tendrá un botón "✕" en la esquina superior derecha
3. Verifica que al hacer clic en "✕" el toast se cierre inmediatamente
4. Si no se cierra con animación, se forzará el cierre en 500ms
        """)
        instructions.setStyleSheet("background: #2D1B42; padding: 15px; border-radius: 8px; color: white;")
        layout.addWidget(instructions)
        
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
                font-weight: bold;
                margin: 5px;
            }}
            QPushButton:hover {{
                background-color: {colors['primary_light']};
            }}
        """)
        
        # Botones de prueba
        self.create_test_button(layout, "🧪 Toast con botón cerrar (Éxito)", self.test_success_closable)
        self.create_test_button(layout, "🧪 Toast con botón cerrar (Error)", self.test_error_closable)
        self.create_test_button(layout, "🧪 Toast con botón cerrar (Advertencia)", self.test_warning_closable)
        self.create_test_button(layout, "🧪 Toast sin botón cerrar (Info)", self.test_info_non_closable)
        self.create_test_button(layout, "🧪 Múltiples toasts con botón cerrar", self.test_multiple_closable)
        
        # Status
        self.status_label = QLabel("✅ Sistema listo para pruebas")
        self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold; padding: 10px;")
        layout.addWidget(self.status_label)
    
    def create_test_button(self, layout, text, callback):
        """Crea un botón de prueba."""
        button = QPushButton(text)
        button.clicked.connect(callback)
        layout.addWidget(button)
    
    def show_instructions(self):
        """Muestra las instrucciones iniciales."""
        show_info_toast("🚀 ¡Haz clic en los botones para probar el cierre!")
        self.status_label.setText("🎯 Prueba el botón ✕ en las notificaciones")
    
    def test_success_closable(self):
        """Prueba toast de éxito con botón cerrar."""
        show_success_toast("✅ ¡Éxito! Prueba el botón ✕ para cerrar", duration=10000)  # 10 segundos para probar
        self.status_label.setText("🧪 Toast de ÉXITO generado - Prueba el botón ✕")
    
    def test_error_closable(self):
        """Prueba toast de error con botón cerrar."""
        show_error_toast("❌ Error crítico - Haz clic en ✕ para cerrar", duration=15000)  # 15 segundos
        self.status_label.setText("🧪 Toast de ERROR generado - Prueba el botón ✕")
    
    def test_warning_closable(self):
        """Prueba toast de advertencia con botón cerrar."""
        show_warning_toast("⚠️ Advertencia importante - Prueba cerrar con ✕", duration=12000)  # 12 segundos
        self.status_label.setText("🧪 Toast de ADVERTENCIA generado - Prueba el botón ✕")
    
    def test_info_non_closable(self):
        """Prueba toast informativo sin botón cerrar."""
        show_info_toast("ℹ️ Información - Este toast NO tiene botón ✕", duration=5000)
        self.status_label.setText("ℹ️ Toast SIN botón cerrar generado")
    
    def test_multiple_closable(self):
        """Prueba múltiples toasts con botón cerrar."""
        self.status_label.setText("🧪 Generando múltiples toasts...")
        
        messages = [
            ("success", "✅ Toast 1 - Prueba cerrar este"),
            ("error", "❌ Toast 2 - Y también este"),
            ("warning", "⚠️ Toast 3 - Y este último"),
        ]
        
        for i, (toast_type, message) in enumerate(messages):
            QTimer.singleShot(i * 800, lambda t=toast_type, m=message: self.show_toast_by_type(t, m))
        
        QTimer.singleShot(3000, lambda: self.status_label.setText("🎯 Múltiples toasts generados - Prueba cerrarlos todos"))
    
    def show_toast_by_type(self, toast_type, message):
        """Muestra un toast según su tipo."""
        duration = 20000  # 20 segundos para tener tiempo de probar
        
        if toast_type == "success":
            show_success_toast(message, duration)
        elif toast_type == "error":
            show_error_toast(message, duration)
        elif toast_type == "warning":
            show_warning_toast(message, duration)
        else:
            show_info_toast(message, duration)


def main():
    """Función principal."""
    app = QApplication(sys.argv)
    
    # Crear y mostrar ventana
    window = CloseButtonTestWindow()
    window.show()
    
    print("🧪 PRUEBA DEL BOTÓN DE CERRAR TOASTS")
    print("=" * 50)
    print("📋 INSTRUCCIONES:")
    print("   1. Haz clic en los botones para generar toasts")
    print("   2. Busca el botón ✕ en cada toast")
    print("   3. Haz clic en ✕ para cerrar")
    print("   4. Verifica que se cierre inmediatamente")
    print("=" * 50)
    print("✅ Si el botón ✕ funciona: ¡PROBLEMA SOLUCIONADO!")
    print("❌ Si el botón ✕ NO funciona: Revisar logs para errores")
    
    # Ejecutar aplicación
    sys.exit(app.exec())


if __name__ == "__main__":
    main()