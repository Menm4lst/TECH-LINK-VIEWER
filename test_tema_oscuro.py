#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test manual para el tema oscuro terminal de TECH LINK VIEWER
Ejecuta una demostración del widget TitleBar con efecto typewriter
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt

# Agregar el path del proyecto
sys.path.insert(0, '.')

from app.theme import apply_dark_theme, Colors, Fonts, get_icon
from app.widgets import TitleBar
from app.delegates import TagDelegate

class TestWindow(QMainWindow):
    """Ventana de prueba para el tema oscuro"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TECH LINK VIEWER - Test Tema Oscuro")
        self.setMinimumSize(800, 400)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Agregar TitleBar con typewriter
        self.title_bar = TitleBar()
        self.title_bar.configure(
            type_speed=100,
            erase_speed=60,
            pause_duration=2000,
            erase_pause=300,
            caret_char="█",
            loop_enabled=True
        )
        layout.addWidget(self.title_bar)
        
        # Área de contenido de prueba
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Botones de prueba con íconos
        buttons_layout = QHBoxLayout()
        
        btn_add = QPushButton("Agregar")
        btn_add.setIcon(get_icon('add'))
        buttons_layout.addWidget(btn_add)
        
        btn_edit = QPushButton("Editar")
        btn_edit.setIcon(get_icon('edit'))
        buttons_layout.addWidget(btn_edit)
        
        btn_delete = QPushButton("Eliminar")
        btn_delete.setIcon(get_icon('delete'))
        buttons_layout.addWidget(btn_delete)
        
        btn_import = QPushButton("Importar")
        btn_import.setIcon(get_icon('import'))
        buttons_layout.addWidget(btn_import)
        
        btn_export = QPushButton("Exportar")
        btn_export.setIcon(get_icon('export'))
        buttons_layout.addWidget(btn_export)
        
        buttons_layout.addStretch()
        content_layout.addLayout(buttons_layout)
        
        # Agregar información del tema
        info_text = f"""
🎨 TEMA OSCURO TERMINAL - TECH LINK VIEWER

🎯 Características implementadas:
• Header con efecto typewriter y caret parpadeante
• Paleta de colores oscura (bg0: {Colors.BG0}, fg: {Colors.FG})
• Íconos SVG con hover effect (fg-dim → accent-neo)
• Fuentes monoespaciadas (JetBrains Mono, Cascadia Code, etc.)
• Estilo QSS completo para todos los widgets
• Delegate para tags como chips estilizadas

⚡ Controles de prueba:
• Los botones tienen íconos que cambian de color al hover
• El header muestra TECH LINK VIEWER con animación typewriter
• Toda la UI usa el tema oscuro terminal consistente

🚀 Estado: Lista para usar en la aplicación principal
        """
        
        from PyQt6.QtWidgets import QTextEdit
        info_display = QTextEdit()
        info_display.setPlainText(info_text.strip())
        info_display.setFont(Fonts.get_monospace_font(Fonts.SIZE_SMALL))
        info_display.setMaximumHeight(300)
        info_display.setReadOnly(True)
        content_layout.addWidget(info_display)
        
        layout.addWidget(content_widget)
        
        # Iniciar animación del header
        self.title_bar.start()

def main():
    app = QApplication(sys.argv)
    
    # Aplicar tema oscuro terminal
    apply_dark_theme(app)
    
    # Crear y mostrar ventana de prueba
    window = TestWindow()
    window.show()
    
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())