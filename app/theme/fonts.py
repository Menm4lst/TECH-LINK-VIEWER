#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración de fuentes para TECH LINK VIEWER
Prioriza fuentes monoespaciadas con fallbacks
"""

from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtCore import QCoreApplication

class Fonts:
    """Configuración de fuentes del tema"""
    
    # Familia de fuentes (prioridad descendente)
    MONOSPACE_FAMILIES = [
        "JetBrains Mono",
        "Cascadia Code", 
        "Fira Code",
        "Consolas",
        "monospace"
    ]
    
    # Tamaños
    SIZE_SMALL = 9
    SIZE_NORMAL = 10
    SIZE_MEDIUM = 12
    SIZE_LARGE = 14
    SIZE_HEADER = 18
    SIZE_TITLE = 20
    
    @staticmethod
    def get_monospace_font(size: int = SIZE_NORMAL, bold: bool = False) -> QFont:
        """Obtiene la mejor fuente monoespaciada disponible"""
        available_families = QFontDatabase.families()
        
        # Buscar la primera fuente disponible en orden de prioridad
        selected_family = "monospace"  # fallback por defecto
        
        for family in Fonts.MONOSPACE_FAMILIES:
            if family in available_families:
                selected_family = family
                break
        
        font = QFont(selected_family, size)
        font.setBold(bold)
        font.setStyleHint(QFont.StyleHint.Monospace)
        font.setFixedPitch(True)
        
        return font
    
    @staticmethod
    def apply_global_font(app):
        """Aplica la fuente monoespaciada globalmente"""
        font = Fonts.get_monospace_font(Fonts.SIZE_NORMAL)
        app.setFont(font)
    
    @staticmethod
    def get_header_font() -> QFont:
        """Fuente para headers/títulos"""
        return Fonts.get_monospace_font(Fonts.SIZE_HEADER, bold=True)
    
    @staticmethod
    def get_title_font() -> QFont:
        """Fuente para el título principal"""
        return Fonts.get_monospace_font(Fonts.SIZE_TITLE, bold=True)
    
    @staticmethod
    def get_subtitle_font() -> QFont:
        """Fuente para subtítulos"""
        return Fonts.get_monospace_font(Fonts.SIZE_MEDIUM, bold=True)
    
    @staticmethod
    def get_small_font() -> QFont:
        """Fuente pequeña para subtítulos"""
        return Fonts.get_monospace_font(Fonts.SIZE_SMALL)
