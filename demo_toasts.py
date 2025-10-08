#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo del Sistema de Notificaciones Toast
Demuestra todas las funcionalidades del sistema de toasts implementado
"""

import sys
import time
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt6.QtCore import QTimer

# Agregar el directorio de la aplicación al path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.widgets import (
    init_toast_system, show_success_toast, show_error_toast,
    show_warning_toast, show_info_toast
)
from app.config import obtener_fluent_colors


class ToastDemo(QMainWindow):
    """Ventana demo para probar el sistema de toasts."""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
        # Inicializar sistema de toasts
        init_toast_system(self)
        
        # Mostrar toast de bienvenida
        QTimer.singleShot(500, self.welcome_toast)
    
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        self.setWindowTitle("🔔 Demo Sistema de Toasts - TECH LINK VIEWER 4.0")
        self.setGeometry(100, 100, 600, 400)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        
        # Título
        title = QLabel("🧪 Demostración del Sistema de Notificaciones Toast")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #9D4EDD; padding: 20px;")
        layout.addWidget(title)
        
        # Botones para cada tipo de toast
        self.create_button(layout, "✅ Mostrar Éxito", self.show_success, "#4CAF50")
        self.create_button(layout, "❌ Mostrar Error", self.show_error, "#F44336")
        self.create_button(layout, "⚠️ Mostrar Advertencia", self.show_warning, "#FF9800")
        self.create_button(layout, "ℹ️ Mostrar Información", self.show_info, "#9D4EDD")
        self.create_button(layout, "🔄 Mostrar Múltiples", self.show_multiple, "#2196F3")
        self.create_button(layout, "🎯 Demo Completo", self.demo_complete, "#9C27B0")
        
        # Aplicar estilo Fluent
        self.apply_fluent_style()
    
    def create_button(self, layout, text, callback, color):
        """Crea un botón estilizado."""
        button = QPushButton(text)
        button.clicked.connect(callback)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                margin: 5px;
            }}
            QPushButton:hover {{
                background-color: {color}DD;
                transform: scale(1.02);
            }}
            QPushButton:pressed {{
                background-color: {color}AA;
            }}
        """)
        layout.addWidget(button)
    
    def apply_fluent_style(self):
        """Aplica el estilo Fluent a la ventana."""
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
        """)
    
    def welcome_toast(self):
        """Toast de bienvenida."""
        show_info_toast("🚀 ¡Bienvenido al Demo de Toasts!")
    
    def show_success(self):
        """Muestra toast de éxito."""
        show_success_toast("💾 ¡Operación completada exitosamente!")
    
    def show_error(self):
        """Muestra toast de error."""
        show_error_toast("❌ Error: No se pudo completar la operación")
    
    def show_warning(self):
        """Muestra toast de advertencia."""
        show_warning_toast("⚠️ Advertencia: Verifica los datos ingresados")
    
    def show_info(self):
        """Muestra toast informativo."""
        show_info_toast("ℹ️ Información: El proceso se ejecutó correctamente")
    
    def show_multiple(self):
        """Muestra múltiples toasts para probar la cola."""
        messages = [
            ("success", "🔗 Enlace 1 creado"),
            ("success", "🔗 Enlace 2 creado"),
            ("warning", "⚠️ URL duplicada detectada"),
            ("success", "🔗 Enlace 3 creado"),
            ("info", "ℹ️ Proceso completado")
        ]
        
        for i, (toast_type, message) in enumerate(messages):
            QTimer.singleShot(i * 800, lambda t=toast_type, m=message: self.delayed_toast(t, m))
    
    def delayed_toast(self, toast_type, message):
        """Muestra un toast con delay."""
        if toast_type == "success":
            show_success_toast(message)
        elif toast_type == "error":
            show_error_toast(message)
        elif toast_type == "warning":
            show_warning_toast(message)
        else:
            show_info_toast(message)
    
    def demo_complete(self):
        """Demo completo que simula operaciones reales."""
        # Simular secuencia de operaciones
        operations = [
            (0, "info", "🔄 Iniciando importación de datos..."),
            (1500, "info", "📂 Validando estructura del archivo..."),
            (3000, "success", "✅ Estructura válida"),
            (4000, "info", "💾 Guardando enlaces..."),
            (5500, "success", "🔗 5 enlaces importados"),
            (6500, "warning", "⚠️ 2 URLs duplicadas omitidas"),
            (7500, "success", "🎉 Importación completada exitosamente!")
        ]
        
        for delay, toast_type, message in operations:
            QTimer.singleShot(delay, lambda t=toast_type, m=message: self.delayed_toast(t, m))


def main():
    """Función principal del demo."""
    app = QApplication(sys.argv)
    
    # Configurar aplicación
    app.setApplicationName("Toast Demo")
    app.setApplicationVersion("1.0")
    
    # Crear y mostrar ventana
    window = ToastDemo()
    window.show()
    
    # Ejecutar aplicación
    sys.exit(app.exec())


if __name__ == "__main__":
    main()