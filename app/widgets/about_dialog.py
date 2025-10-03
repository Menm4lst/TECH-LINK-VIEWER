#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diálogo Acerca de para TECH LINK VIEWER
Información del desarrollador y aplicación
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QFrame, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap, QPainter, QBrush, QColor

from ..theme.colors import Colors
from ..theme.fonts import Fonts
from ..theme.icons import get_icon


class AboutDialog(QDialog):
    """Diálogo Acerca de con estilo terminal"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Acerca de TLV 4.0")
        self.setModal(True)
        self.setFixedSize(650, 550)  # Aumentado más para dar espacio al texto
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {Colors.BG0};
                border: 3px solid {Colors.ACCENT_CYAN};
                border-radius: 8px;
            }}
            QLabel {{
                color: {Colors.FG};
                background-color: transparent;
                font-weight: bold;
            }}
            QLabel[class="header"] {{
                color: {Colors.ACCENT_CYAN};
                background-color: {Colors.BG1};
                border: 2px solid {Colors.ACCENT_CYAN};
                padding: 12px;
                font-size: 18px;
                font-weight: bold;
            }}
            QLabel[class="description"] {{
                color: {Colors.FG};
                font-size: 14px;
                padding: 4px;
            }}
            QLabel[class="version"] {{
                color: {Colors.ACCENT_NEO};
                font-size: 12px;
                padding: 2px;
            }}
            QLabel[class="dev-header"] {{
                color: {Colors.ACCENT_CYAN};
                font-size: 16px;
                font-weight: bold;
                padding: 8px 0px;
            }}
            QLabel[class="dev-name"] {{
                color: {Colors.ACCENT_NEO};
                font-size: 16px;
                font-weight: bold;
                padding: 8px 12px;
                margin: 4px 0px;
                background-color: {Colors.BG2};
                border: 1px solid {Colors.ACCENT_NEO};
                border-radius: 4px;
                min-height: 24px;
                qproperty-wordWrap: false;
            }}
            QLabel[class="dev-info"] {{
                color: {Colors.FG};
                font-size: 13px;
                padding: 3px;
            }}
            QPushButton {{
                background-color: {Colors.BG2};
                color: {Colors.FG};
                border: 2px solid {Colors.ACCENT_CYAN};
                padding: 10px 20px;
                border-radius: 6px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: {Colors.ACCENT_NEO};
                color: {Colors.BG0};
                border-color: {Colors.ACCENT_NEO};
            }}
            QPushButton:pressed {{
                background-color: {Colors.ACCENT_CYAN};
                color: {Colors.BG0};
            }}
            QFrame {{
                background-color: transparent;
                border: 1px solid {Colors.FG_DIM};
            }}
        """)
        
        self._setup_ui()
        self._setup_animations()
    
    def _setup_ui(self):
        """Configura la interfaz del diálogo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)  # Márgenes más grandes
        layout.setSpacing(20)  # Espaciado aumentado
        
        # Header con título principal
        self._create_header(layout)
        
        # Información de la aplicación
        self._create_app_info(layout)
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet(f"color: {Colors.FG_DIM};")
        layout.addWidget(separator)
        
        # Información del desarrollador
        self._create_developer_info(layout)
        
        # Spacer
        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)
        
        # Botones
        self._create_buttons(layout)
    
    def _create_header(self, layout):
        """Crea el header con el título principal"""
        header_layout = QHBoxLayout()
        
        # Título con efecto typewriter
        self.title_label = QLabel("TECH LINK VIEWER 4.0")
        self.title_label.setFont(Fonts.get_monospace_font(Fonts.SIZE_LARGE, bold=True))
        self.title_label.setProperty("class", "header")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        header_layout.addWidget(self.title_label)
        layout.addLayout(header_layout)
    
    def _create_app_info(self, layout):
        """Crea la información de la aplicación"""
        info_layout = QVBoxLayout()
        info_layout.setSpacing(8)  # Espaciado aumentado
        
        # Descripción
        desc_label = QLabel("📋 Gestor avanzado de enlaces con interfaz terminal")
        desc_label.setFont(Fonts.get_monospace_font(Fonts.SIZE_MEDIUM))
        desc_label.setProperty("class", "description")
        info_layout.addWidget(desc_label)
        
        # Versión
        version_label = QLabel("🔧 Versión: 4.0.0 - Terminal Edition")
        version_label.setFont(Fonts.get_monospace_font(Fonts.SIZE_SMALL))
        version_label.setProperty("class", "version")
        info_layout.addWidget(version_label)
        
        # Framework
        framework_label = QLabel("⚙️  Framework: PyQt6 6.7.1")
        framework_label.setFont(Fonts.get_monospace_font(Fonts.SIZE_SMALL))
        framework_label.setProperty("class", "version")
        info_layout.addWidget(framework_label)
        
        # Características
        features_label = QLabel("✨ Tema oscuro terminal • Iconos SVG • Efectos typewriter")
        features_label.setFont(Fonts.get_monospace_font(Fonts.SIZE_SMALL))
        features_label.setProperty("class", "version")
        info_layout.addWidget(features_label)
        
        layout.addLayout(info_layout)
    
    def _create_developer_info(self, layout):
        """Crea la información del desarrollador"""
        dev_layout = QVBoxLayout()
        dev_layout.setSpacing(8)  # Espaciado aumentado
        
        # Header desarrollador
        dev_header = QLabel("👨‍💻 DESARROLLADOR")
        dev_header.setFont(Fonts.get_monospace_font(Fonts.SIZE_MEDIUM, bold=True))
        dev_header.setProperty("class", "dev-header")
        dev_layout.addWidget(dev_header)
        
        # Nombre del desarrollador
        name_label = QLabel("🚀 Antware")
        name_label.setFont(Fonts.get_monospace_font(Fonts.SIZE_MEDIUM, bold=True))
        name_label.setProperty("class", "dev-name")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setMinimumHeight(40)  # Altura mínima garantizada
        name_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        dev_layout.addWidget(name_label)
        
        # Título profesional
        title_label = QLabel("💻 Desarrollador de Software")
        title_label.setFont(Fonts.get_monospace_font(Fonts.SIZE_SMALL))
        title_label.setProperty("class", "dev-info")
        dev_layout.addWidget(title_label)
        
        # Año
        year_label = QLabel("📅 © 2025 - Hecho con ❤️  y ☕")
        year_label.setFont(Fonts.get_monospace_font(Fonts.SIZE_SMALL))
        year_label.setProperty("class", "dev-info")
        dev_layout.addWidget(year_label)
        
        layout.addLayout(dev_layout)
    
    def _create_buttons(self, layout):
        """Crea los botones del diálogo"""
        button_layout = QHBoxLayout()
        
        # Botón Cerrar
        close_button = QPushButton("Cerrar")
        close_button.setFont(Fonts.get_monospace_font(Fonts.SIZE_SMALL, bold=True))
        close_button.clicked.connect(self.accept)
        close_button.setDefault(True)
        
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
    
    def _setup_animations(self):
        """Configura las animaciones del diálogo"""
        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self._toggle_title_glow)
        self.blink_timer.start(1500)  # Parpadeo cada 1.5 segundos
        self.title_glow = False
    
    def _toggle_title_glow(self):
        """Alterna el efecto de brillo en el título"""
        if self.title_glow:
            # Estado normal - Cyan
            self.title_label.setStyleSheet(f"""
                color: {Colors.ACCENT_CYAN};
                padding: 12px;
                border: 3px solid {Colors.ACCENT_CYAN};
                background-color: {Colors.BG0};
                border-radius: 6px;
                font-weight: bold;
            """)
        else:
            # Estado brillante - Verde neón
            self.title_label.setStyleSheet(f"""
                color: {Colors.ACCENT_NEO};
                padding: 12px;
                border: 3px solid {Colors.ACCENT_NEO};
                background-color: {Colors.BG2};
                border-radius: 6px;
                font-weight: bold;
                text-decoration: none;
            """)
        
        self.title_glow = not self.title_glow
    
    def closeEvent(self, event):
        """Maneja el cierre del diálogo"""
        if hasattr(self, 'blink_timer'):
            self.blink_timer.stop()
        super().closeEvent(event)