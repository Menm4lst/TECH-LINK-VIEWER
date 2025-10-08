#!/usr/bin/env python3
"""
Prueba SIMPLE del botón de cerrar
"""
import sys
import os

# Agregar el directorio raíz del proyecto al path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import Qt
from app.widgets.toast_notification import ToastManager

class SimpleTest(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PRUEBA SIMPLE - Botón Cerrar Toast")
        self.setGeometry(100, 100, 400, 200)
        
        # Layout
        layout = QVBoxLayout()
        
        # Botón para crear toast
        btn = QPushButton("🍞 Crear Toast de Prueba")
        btn.clicked.connect(self.create_test_toast)
        layout.addWidget(btn)
        
        # Instrucciones
        instructions = QPushButton("INSTRUCCIONES:\n1. Haz clic arriba para crear toast\n2. Haz clic en el ✕ del toast\n3. El toast debería desaparecer INMEDIATAMENTE")
        instructions.setEnabled(False)
        instructions.setStyleSheet("QPushButton:disabled { color: #333; background: #f0f0f0; }")
        layout.addWidget(instructions)
        
        self.setLayout(layout)
        
        # Crear manager de toasts
        self.toast_manager = ToastManager(self)
        
    def create_test_toast(self):
        print("🍞 Creando toast de prueba...")
        self.toast_manager.show_info(
            message="PRUEBA BOTÓN CERRAR: Haz clic en el ✕ para cerrar este toast",
            duration=30000,  # 30 segundos para dar tiempo de probar
            closable=True
        )
        print("✅ Toast creado - intenta cerrarlo con el ✕")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Aplicar estilo básico
    app.setStyleSheet("""
        QWidget {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 11px;
        }
        QPushButton {
            padding: 10px;
            margin: 5px;
            border: 2px solid #9D4EDD;
            border-radius: 8px;
            background-color: #9D4EDD;
            color: white;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #8B3ACD;
        }
    """)
    
    test_widget = SimpleTest()
    test_widget.show()
    
    print("🚀 PRUEBA INICIADA")
    print("📋 PASOS:")
    print("   1. Haz clic en 'Crear Toast de Prueba'")
    print("   2. Busca el toast que aparece")
    print("   3. Haz clic en el ✕ (botón cerrar)")
    print("   4. El toast debe desaparecer inmediatamente")
    print("🔍 Revisa los logs en consola para debug")
    print("="*50)
    
    sys.exit(app.exec())