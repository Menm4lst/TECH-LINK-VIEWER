#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Widget de Favoritos para TECH LINK VIEWER 4.0
Panel lateral para acceso rápido a enlaces favoritos
"""

import logging
from typing import List, Dict, Any
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QListWidget, QListWidgetItem, QFrame, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor

from ..theme import Colors, Fonts, get_icon
from ..config import (
    obtener_fluent_colors, obtener_fluent_typography, obtener_fluent_spacing,
    get_fluent_color, get_fluent_font_size, get_fluent_spacing
)

logger = logging.getLogger(__name__)


class FavoritosWidget(QWidget):
    """Widget para mostrar y gestionar enlaces favoritos"""
    
    # Señales
    favorito_seleccionado = pyqtSignal(str)  # ID del enlace
    favorito_eliminado = pyqtSignal(str)     # ID del enlace
    abrir_enlace = pyqtSignal(str)          # ID del enlace
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.favoritos_data = []
        self.repositorio = None  # Se asignará desde el padre
        
        self._setup_ui()
        self._aplicar_estilos()
        
        logger.info("Widget de favoritos inicializado")
    
    def _setup_ui(self):
        """Configura la interfaz de usuario"""
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(8, 8, 8, 8)
        layout_principal.setSpacing(8)
        
        # Header con título y contador
        self._crear_header(layout_principal)
        
        # Lista de favoritos
        self._crear_lista_favoritos(layout_principal)
        
        # Botones de acción
        self._crear_botones_accion(layout_principal)
    
    def _crear_header(self, layout_padre):
        """Crea el header con título y contador"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Shape.NoFrame)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(4)
        
        # Título
        titulo_label = QLabel("⭐ Favoritos")
        titulo_label.setObjectName("titulo_favoritos")
        titulo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        header_layout.addWidget(titulo_label)
        
        # Contador
        self.contador_label = QLabel("0 enlaces")
        self.contador_label.setObjectName("contador_favoritos")
        self.contador_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.contador_label.setFont(QFont("Segoe UI", 9))
        header_layout.addWidget(self.contador_label)
        
        layout_padre.addWidget(header_frame)
    
    def _crear_lista_favoritos(self, layout_padre):
        """Crea la lista de enlaces favoritos"""
        # Área de scroll para la lista
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFrameStyle(QFrame.Shape.NoFrame)
        
        # Widget contenedor para los favoritos
        self.lista_widget = QWidget()
        self.lista_layout = QVBoxLayout(self.lista_widget)
        self.lista_layout.setContentsMargins(0, 0, 0, 0)
        self.lista_layout.setSpacing(4)
        self.lista_layout.addStretch()  # Para empujar items hacia arriba
        
        scroll_area.setWidget(self.lista_widget)
        layout_padre.addWidget(scroll_area)
    
    def _crear_botones_accion(self, layout_padre):
        """Crea los botones de acción"""
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(4)
        
        # Botón refrescar
        self.btn_refrescar = QPushButton("🔄")
        self.btn_refrescar.setToolTip("Refrescar favoritos")
        self.btn_refrescar.setFixedSize(30, 30)
        self.btn_refrescar.clicked.connect(self.refrescar_favoritos)
        
        # Botón limpiar todos
        self.btn_limpiar = QPushButton("🗑️")
        self.btn_limpiar.setToolTip("Desmarcar todos los favoritos")
        self.btn_limpiar.setFixedSize(30, 30)
        self.btn_limpiar.clicked.connect(self._confirmar_limpiar_todos)
        
        botones_layout.addWidget(self.btn_refrescar)
        botones_layout.addWidget(self.btn_limpiar)
        botones_layout.addStretch()
        
        layout_padre.addLayout(botones_layout)
    
    def _aplicar_estilos(self):
        """Aplica estilos al widget"""
        colors = obtener_fluent_colors()
        spacing = obtener_fluent_spacing()
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {colors['surface_secondary']};
                color: {colors['text_primary']};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            
            QLabel#titulo_favoritos {{
                color: {colors['primary']};
                font-weight: bold;
                padding: 8px;
                border-bottom: 2px solid {colors['primary']};
                margin-bottom: 8px;
            }}
            
            QLabel#contador_favoritos {{
                color: {colors['text_secondary']};
                font-size: 10px;
                margin-bottom: 8px;
            }}
            
            QPushButton {{
                background-color: {colors['surface_primary']};
                border: 1px solid {colors['stroke_primary']};
                border-radius: 6px;
                padding: 6px;
                font-weight: bold;
            }}
            
            QPushButton:hover {{
                background-color: {colors['surface_elevated']};
                border-color: {colors['primary']};
            }}
            
            QPushButton:pressed {{
                background-color: {colors['primary']};
                color: {colors['text_on_accent']};
            }}
            
            QScrollArea {{
                border: 1px solid {colors['stroke_primary']};
                border-radius: 8px;
                background-color: {colors['surface_primary']};
            }}
        """)
    
    def set_repositorio(self, repositorio):
        """Asigna el repositorio de datos"""
        self.repositorio = repositorio
        self.refrescar_favoritos()
    
    def refrescar_favoritos(self):
        """Refresca la lista de favoritos"""
        if not self.repositorio:
            return
        
        # Obtener favoritos del repositorio
        self.favoritos_data = self.repositorio.obtener_favoritos()
        
        # Limpiar lista actual
        self._limpiar_lista()
        
        # Agregar nuevos items
        for enlace in self.favoritos_data:
            self._agregar_item_favorito(enlace)
        
        # Actualizar contador
        total = len(self.favoritos_data)
        texto_contador = f"{total} enlace{'s' if total != 1 else ''}"
        self.contador_label.setText(texto_contador)
        
        logger.info(f"Favoritos refrescados: {total} enlaces")
    
    def _limpiar_lista(self):
        """Limpia todos los items de la lista"""
        # Eliminar todos los widgets excepto el stretch
        while self.lista_layout.count() > 1:
            child = self.lista_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def _agregar_item_favorito(self, enlace):
        """Agrega un item favorito a la lista"""
        item_widget = FavoritoItemWidget(enlace, self)
        
        # Conectar señales
        item_widget.clic_enlace.connect(self.abrir_enlace.emit)
        item_widget.eliminar_favorito.connect(self._eliminar_favorito)
        item_widget.seleccionado.connect(self.favorito_seleccionado.emit)
        
        # Insertar antes del stretch
        self.lista_layout.insertWidget(self.lista_layout.count() - 1, item_widget)
    
    def _eliminar_favorito(self, enlace_id):
        """Elimina un favorito"""
        if self.repositorio:
            if self.repositorio.desmarcar_favorito(enlace_id):
                self.repositorio.guardar()
                self.refrescar_favoritos()
                self.favorito_eliminado.emit(enlace_id)
                logger.info(f"Favorito eliminado: {enlace_id}")
    
    def _confirmar_limpiar_todos(self):
        """Confirma y limpia todos los favoritos"""
        from PyQt6.QtWidgets import QMessageBox
        
        if not self.favoritos_data:
            return
        
        reply = QMessageBox.question(
            self, 
            "Confirmar", 
            f"¿Desmarcar todos los {len(self.favoritos_data)} favoritos?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self._limpiar_todos_favoritos()
    
    def _limpiar_todos_favoritos(self):
        """Desmarca todos los favoritos"""
        if not self.repositorio:
            return
        
        count = 0
        for enlace in self.favoritos_data:
            if self.repositorio.desmarcar_favorito(enlace['id']):
                count += 1
        
        if count > 0:
            self.repositorio.guardar()
            self.refrescar_favoritos()
            logger.info(f"Limpiados {count} favoritos")


class FavoritoItemWidget(QWidget):
    """Widget individual para mostrar un enlace favorito"""
    
    # Señales
    clic_enlace = pyqtSignal(str)        # ID del enlace
    eliminar_favorito = pyqtSignal(str)  # ID del enlace
    seleccionado = pyqtSignal(str)       # ID del enlace
    
    def __init__(self, enlace, parent=None):
        super().__init__(parent)
        self.enlace = enlace
        self.enlace_id = enlace.get('id', '')
        
        self._setup_ui()
        self._aplicar_estilos()
    
    def _setup_ui(self):
        """Configura la interfaz del item"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(4)
        
        # Header con título y botón eliminar
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Título (clickeable)
        self.titulo_label = QLabel(self.enlace.get('titulo', 'Sin título'))
        self.titulo_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self.titulo_label.setWordWrap(True)
        self.titulo_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.titulo_label.mousePressEvent = self._clic_titulo
        
        # Botón eliminar
        self.btn_eliminar = QPushButton("×")
        self.btn_eliminar.setFixedSize(20, 20)
        self.btn_eliminar.setToolTip("Desmarcar favorito")
        self.btn_eliminar.clicked.connect(lambda: self.eliminar_favorito.emit(self.enlace_id))
        
        header_layout.addWidget(self.titulo_label)
        header_layout.addWidget(self.btn_eliminar)
        
        # Información adicional
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(2)
        
        # Categoría
        categoria = self.enlace.get('categoria', '')
        if categoria:
            categoria_label = QLabel(f"📁 {categoria}")
            categoria_label.setFont(QFont("Segoe UI", 8))
            categoria_label.setObjectName("categoria_label")
            info_layout.addWidget(categoria_label)
        
        # Tags
        tags = self.enlace.get('tags', [])
        if tags:
            tags_text = " ".join([f"#{tag}" for tag in tags[:3]])  # Max 3 tags
            if len(tags) > 3:
                tags_text += f" +{len(tags)-3}"
            tags_label = QLabel(tags_text)
            tags_label.setFont(QFont("Segoe UI", 8))
            tags_label.setObjectName("tags_label")
            info_layout.addWidget(tags_label)
        
        layout.addLayout(header_layout)
        layout.addLayout(info_layout)
    
    def _aplicar_estilos(self):
        """Aplica estilos al item"""
        colors = obtener_fluent_colors()
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {colors['surface_primary']};
                border: 1px solid {colors['stroke_primary']};
                border-radius: 8px;
                margin: 2px;
            }}
            
            QWidget:hover {{
                background-color: {colors['surface_elevated']};
                border-color: {colors['primary']};
            }}
            
            QLabel {{
                color: {colors['text_primary']};
                border: none;
                background: transparent;
            }}
            
            QLabel#categoria_label {{
                color: {colors['text_secondary']};
            }}
            
            QLabel#tags_label {{
                color: {colors['primary']};
                font-style: italic;
            }}
            
            QPushButton {{
                background-color: transparent;
                border: 1px solid {colors['stroke_primary']};
                border-radius: 10px;
                color: {colors['text_secondary']};
                font-weight: bold;
                font-size: 12px;
            }}
            
            QPushButton:hover {{
                background-color: {colors['error']};
                color: {colors['text_on_accent']};
                border-color: {colors['error']};
            }}
        """)
    
    def _clic_titulo(self, event):
        """Maneja el clic en el título"""
        self.clic_enlace.emit(self.enlace_id)
        self.seleccionado.emit(self.enlace_id)