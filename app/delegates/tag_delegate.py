#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Delegate para renderizar tags como chips estilizadas en TECH LINK VIEWER
Personaliza la apariencia de tags en la tabla con estilo píldoras
"""

from PyQt6.QtWidgets import QStyledItemDelegate, QStyle, QStyleOptionViewItem
from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFontMetrics
from ..theme.colors import Colors
from ..theme.fonts import Fonts

class TagDelegate(QStyledItemDelegate):
    """
    Delegate personalizado para renderizar tags como chips/píldoras
    Renderiza una lista de tags separadas por comas como elementos visuales individuales
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Configuración de estilo
        self.chip_padding = 8
        self.chip_margin = 6  # Aumentado de 4 a 6
        self.chip_height = 28  # Aumentado de 24 a 28
        self.border_radius = 14  # Aumentado de 12 a 14
        self.border_width = 1
        
        # Colores
        self.bg_color = QColor(Colors.BG2)
        self.border_color = QColor(Colors.BORDER)
        self.text_color = QColor(Colors.FG_DIM)
        self.hover_border_color = QColor(Colors.ACCENT_CYAN)
        self.hover_bg_color = QColor(Colors.HOVER)
    
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index):
        """Renderiza las tags como chips estilizadas"""
        
        # Obtener el texto de tags
        text = index.data(Qt.ItemDataRole.DisplayRole)
        if not text or not isinstance(text, str):
            return
        
        # Dividir tags por comas y limpiar espacios
        tags = [tag.strip() for tag in text.split(',') if tag.strip()]
        if not tags:
            return
        
        # Configurar painter
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        
        # Obtener fuente y métricas
        font = Fonts.get_monospace_font(Fonts.SIZE_SMALL)
        painter.setFont(font)
        font_metrics = QFontMetrics(font)
        
        # Configurar área de dibujo
        rect = option.rect
        x = rect.x() + self.chip_margin
        y = rect.y() + (rect.height() - self.chip_height) // 2
        max_width = rect.width() - (self.chip_margin * 2)
        
        # Estado hover/selección
        is_hovered = option.state & QStyle.StateFlag.State_MouseOver
        is_selected = option.state & QStyle.StateFlag.State_Selected
        
        # Renderizar cada tag
        for i, tag in enumerate(tags):
            # Calcular ancho del chip
            text_width = font_metrics.horizontalAdvance(tag)
            chip_width = text_width + (self.chip_padding * 2)
            
            # Verificar si cabe en la línea actual
            if x + chip_width > rect.x() + max_width:
                # No cabe, truncar con "..."
                if i > 0:  # Solo si ya renderizamos al menos un chip
                    # Renderizar "..." para indicar más tags
                    dots_width = font_metrics.horizontalAdvance("...")
                    dots_chip_width = dots_width + (self.chip_padding * 2)
                    
                    if x + dots_chip_width <= rect.x() + max_width:
                        self._draw_chip(painter, x, y, dots_chip_width, "...", 
                                      is_hovered, is_selected, font_metrics)
                break
            
            # Renderizar el chip
            self._draw_chip(painter, x, y, chip_width, tag, 
                          is_hovered, is_selected, font_metrics)
            
            # Avanzar posición x
            x += chip_width + self.chip_margin
        
        painter.restore()
    
    def _draw_chip(self, painter: QPainter, x: int, y: int, width: int, 
                   text: str, is_hovered: bool, is_selected: bool, 
                   font_metrics: QFontMetrics):
        """Dibuja un chip individual"""
        
        # Definir rectángulo del chip
        chip_rect = QRect(x, y, width, self.chip_height)
        
        # Seleccionar colores según estado
        if is_selected:
            bg_color = QColor(Colors.SELECTED)
            border_color = QColor(Colors.ACCENT_NEO)
            text_color = QColor(Colors.FG)
        elif is_hovered:
            bg_color = self.hover_bg_color
            border_color = self.hover_border_color
            text_color = QColor(Colors.FG)
        else:
            bg_color = self.bg_color
            border_color = self.border_color
            text_color = self.text_color
        
        # Dibujar fondo del chip
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(bg_color))
        painter.drawRoundedRect(chip_rect, self.border_radius, self.border_radius)
        
        # Dibujar borde del chip
        pen = QPen(border_color, self.border_width)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(chip_rect, self.border_radius, self.border_radius)
        
        # Dibujar texto centrado
        painter.setPen(QPen(text_color))
        text_rect = QRect(x + self.chip_padding, y, 
                         width - (self.chip_padding * 2), self.chip_height)
        
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, text)
    
    def sizeHint(self, option: QStyleOptionViewItem, index) -> QSize:
        """Retorna el tamaño sugerido para el item"""
        
        # Obtener texto
        text = index.data(Qt.ItemDataRole.DisplayRole)
        if not text or not isinstance(text, str):
            return QSize(0, self.chip_height + (self.chip_margin * 2))  # Altura aumentada
        
        # Dividir tags
        tags = [tag.strip() for tag in text.split(',') if tag.strip()]
        if not tags:
            return QSize(0, self.chip_height + (self.chip_margin * 2))  # Altura aumentada
        
        # Calcular ancho necesario
        font = Fonts.get_monospace_font(Fonts.SIZE_SMALL)
        font_metrics = QFontMetrics(font)
        
        total_width = self.chip_margin
        for tag in tags:
            text_width = font_metrics.horizontalAdvance(tag)
            chip_width = text_width + (self.chip_padding * 2)
            total_width += chip_width + self.chip_margin
        
        return QSize(total_width, self.chip_height + (self.chip_margin * 2))  # Altura aumentada