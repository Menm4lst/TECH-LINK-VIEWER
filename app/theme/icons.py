#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Íconos SVG inline para TECH LINK VIEWER
Estilo terminal con colores fg-dim que cambian a accent-neo en hover
"""

from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import QByteArray, QSize, Qt
from .colors import Colors

class Icons:
    """Generador de íconos SVG con estados hover"""
    
    # Plantilla base SVG
    SVG_TEMPLATE = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    {content}
</svg>'''
    
    # Definiciones de íconos (contenido SVG)
    ICONS = {
        'search': '''
            <circle cx="11" cy="11" r="8" stroke="{color}" stroke-width="2"/>
            <path d="M21 21l-4.35-4.35" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
        ''',
        
        'add': '''
            <circle cx="12" cy="12" r="10" stroke="{color}" stroke-width="2"/>
            <line x1="12" y1="8" x2="12" y2="16" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
            <line x1="8" y1="12" x2="16" y2="12" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
        ''',
        
        'edit': '''
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        ''',
        
        'delete': '''
            <polyline points="3,6 5,6 21,6" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="10" y1="11" x2="10" y2="17" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
            <line x1="14" y1="11" x2="14" y2="17" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
        ''',
        
        'import': '''
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <polyline points="14,2 14,8 20,8" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="12" y1="18" x2="12" y2="12" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
            <polyline points="9,15 12,12 15,15" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        ''',
        
        'export': '''
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <polyline points="14,2 14,8 20,8" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="12" y1="12" x2="12" y2="18" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
            <polyline points="15,15 12,18 9,15" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        ''',
        
        'link': '''
            <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        ''',
        
        'tag': '''
            <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="7" y1="7" x2="7.01" y2="7" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
        ''',
        
        'info': '''
            <circle cx="12" cy="12" r="10" stroke="{color}" stroke-width="2"/>
            <line x1="12" y1="16" x2="12" y2="12" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
            <line x1="12" y1="8" x2="12.01" y2="8" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
        ''',
        
        'settings': '''
            <circle cx="12" cy="12" r="3" stroke="{color}" stroke-width="2"/>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        ''',
        
        'refresh': '''
            <polyline points="23,4 23,10 17,10" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <polyline points="1,20 1,14 7,14" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        ''',
        
        'help': '''
            <circle cx="12" cy="12" r="10" stroke="{color}" stroke-width="2"/>
            <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="12" y1="17" x2="12.01" y2="17" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
        ''',
        
        'star': '''
            <polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        ''',
        
        'star_filled': '''
            <polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="{color}"/>
        '''
    }
    
    @staticmethod
    def create_icon(name: str, color: str = Colors.FG_DIM, size: int = 24) -> QIcon:
        """Crea un ícono SVG con el color especificado"""
        if name not in Icons.ICONS:
            name = 'link'  # ícono por defecto
        
        # Generar SVG con color
        svg_content = Icons.ICONS[name].format(color=color)
        svg_data = Icons.SVG_TEMPLATE.format(content=svg_content)
        
        # Crear QIcon desde SVG
        svg_bytes = QByteArray(svg_data.encode('utf-8'))
        renderer = QSvgRenderer(svg_bytes)
        
        pixmap = QPixmap(QSize(size, size))
        pixmap.fill(Qt.GlobalColor.transparent)  # Fondo transparente
        
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        
        icon = QIcon(pixmap)
        return icon
    
    @staticmethod
    def create_hover_icon(name: str, normal_color: str = Colors.FG_DIM, 
                         hover_color: str = Colors.ACCENT_NEO, size: int = 24) -> QIcon:
        """Crea un ícono con estados normal y hover"""
        icon = QIcon()
        
        # Estado normal
        normal_icon = Icons.create_icon(name, normal_color, size)
        icon.addPixmap(normal_icon.pixmap(QSize(size, size)), QIcon.Mode.Normal)
        
        # Estado hover (active)
        hover_icon = Icons.create_icon(name, hover_color, size)
        icon.addPixmap(hover_icon.pixmap(QSize(size, size)), QIcon.Mode.Active)
        
        return icon
    
    @staticmethod
    def get_all_icons() -> dict:
        """Retorna todos los íconos disponibles con hover effect"""
        icons = {}
        for name in Icons.ICONS.keys():
            icons[name] = Icons.create_hover_icon(name)
        return icons

# Función de conveniencia para obtener íconos comunes
def get_icon(name: str) -> QIcon:
    """Obtiene un ícono con efecto hover"""
    return Icons.create_hover_icon(name)