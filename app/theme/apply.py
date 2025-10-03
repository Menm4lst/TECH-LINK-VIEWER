#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicador de tema oscuro para TECH LINK VIEWER
Función principal para aplicar el tema completo
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from .colors import Colors
from .fonts import Fonts

# Importar la clase DarkTheme desde el módulo dark.qss
import os
from pathlib import Path

class DarkTheme:
    """Cargador de estilos QSS desde archivo"""
    
    @staticmethod
    def get_main_stylesheet() -> str:
        """Carga y retorna el stylesheet desde dark.qss"""
        # Obtener ruta del archivo de estilos
        current_dir = Path(__file__).parent
        qss_file = current_dir / "dark.qss"
        
        if qss_file.exists():
            with open(qss_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Reemplazar tokens de colores
                content = content.replace('{Colors.BG0}', Colors.BG0)
                content = content.replace('{Colors.BG1}', Colors.BG1)
                content = content.replace('{Colors.BG2}', Colors.BG2)
                content = content.replace('{Colors.FG}', Colors.FG)
                content = content.replace('{Colors.FG_DIM}', Colors.FG_DIM)
                content = content.replace('{Colors.ACCENT_NEO}', Colors.ACCENT_NEO)
                content = content.replace('{Colors.ACCENT_CYAN}', Colors.ACCENT_CYAN)
                content = content.replace('{Colors.ACCENT_AMBER}', Colors.ACCENT_AMBER)
                content = content.replace('{Colors.BORDER}', Colors.BORDER)
                content = content.replace('{Colors.BORDER_LIGHT}', Colors.BORDER_LIGHT)
                content = content.replace('{Colors.HOVER}', Colors.HOVER)
                content = content.replace('{Colors.PRESSED}', Colors.PRESSED)
                content = content.replace('{Colors.SELECTED}', Colors.SELECTED)
                content = content.replace('{Colors.SHADOW}', Colors.SHADOW)
                content = content.replace('{Colors.GLOW_CYAN}', Colors.GLOW_CYAN)
                content = content.replace('{Colors.GLOW_NEO}', Colors.GLOW_NEO)
                return content
        
        # Fallback si no se encuentra el archivo
        return f"""
QWidget {{
    background-color: {Colors.BG0};
    color: {Colors.FG};
    font-family: "JetBrains Mono", "Cascadia Code", "Fira Code", "Consolas", monospace;
}}
"""

def apply_dark_theme(app: QApplication):
    """
    Aplica el tema oscuro completo a la aplicación
    
    Args:
        app: Instancia de QApplication
    """
    # Aplicar fuente global monoespaciada
    Fonts.apply_global_font(app)
    
    # Aplicar stylesheet principal
    app.setStyleSheet(DarkTheme.get_main_stylesheet())
    
    # Configurar paleta global como fallback
    from PyQt6.QtGui import QPalette, QColor
    
    palette = QPalette()
    
    # Colores de fondo
    palette.setColor(QPalette.ColorRole.Window, QColor(Colors.BG0))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(Colors.FG))
    palette.setColor(QPalette.ColorRole.Base, QColor(Colors.BG1))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(Colors.BG2))
    
    # Colores de texto
    palette.setColor(QPalette.ColorRole.Text, QColor(Colors.FG))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(Colors.FG))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(Colors.FG_DIM))
    
    # Colores de botones
    palette.setColor(QPalette.ColorRole.Button, QColor(Colors.BG2))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(Colors.FG))
    
    # Colores de selección
    palette.setColor(QPalette.ColorRole.Highlight, QColor(Colors.ACCENT_CYAN))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(Colors.FG))
    
    # Colores deshabilitados
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor(Colors.FG_DIM))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(Colors.FG_DIM))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(Colors.FG_DIM))
    
    app.setPalette(palette)

def get_theme_info() -> dict:
    """
    Retorna información sobre el tema aplicado
    
    Returns:
        dict: Información del tema con colores y configuración
    """
    return {
        "name": "Dark Terminal Theme",
        "version": "1.0.0",
        "colors": {
            "background": Colors.BG0,
            "surface": Colors.BG1,
            "input": Colors.BG2,
            "text": Colors.FG,
            "text_secondary": Colors.FG_DIM,
            "accent_primary": Colors.ACCENT_NEO,
            "accent_secondary": Colors.ACCENT_CYAN,
            "warning": Colors.ACCENT_AMBER
        },
        "fonts": {
            "primary": "JetBrains Mono, Cascadia Code, Fira Code, Consolas, monospace",
            "sizes": {
                "small": Fonts.SIZE_SMALL,
                "normal": Fonts.SIZE_NORMAL,
                "medium": Fonts.SIZE_MEDIUM,
                "large": Fonts.SIZE_LARGE,
                "header": Fonts.SIZE_HEADER,
                "title": Fonts.SIZE_TITLE
            }
        },
        "effects": {
            "border_radius": "8px",
            "shadow": "0 8px 24px rgba(0,0,0,.45)",
            "glow_intensity": "8px",
            "padding": "8px 12px 16px"
        }
    }