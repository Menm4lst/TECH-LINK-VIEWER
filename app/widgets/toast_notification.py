#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Notificaciones Toast para TECH LINK VIEWER 4.0
Notificaciones modernas con diseño Fluent y animaciones suaves
"""

import logging
from enum import Enum
from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, 
    QGraphicsDropShadowEffect, QFrame, QSizePolicy
)
from PyQt6.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve, 
    pyqtSignal, QPoint, QRect, QParallelAnimationGroup
)
from PyQt6.QtGui import QFont, QPainter, QPalette, QColor

from ..config import (
    get_fluent_color, get_fluent_font_size, get_fluent_spacing,
    get_fluent_border_radius, obtener_fluent_colors
)

logger = logging.getLogger(__name__)


class ToastType(Enum):
    """Tipos de notificaciones toast."""
    SUCCESS = "success"
    ERROR = "error" 
    WARNING = "warning"
    INFO = "info"


class ToastNotification(QFrame):
    """
    Widget de notificación toast con diseño Fluent.
    
    Características:
    - Animaciones de entrada/salida suaves
    - Auto-hide configurable
    - Diferentes tipos con iconos y colores
    - Efecto de sombra y blur
    - Posición automática en la ventana padre
    """
    
    # Señales
    clicked = pyqtSignal()
    closed = pyqtSignal()
    
    def __init__(
        self, 
        parent: QWidget,
        message: str,
        toast_type: ToastType = ToastType.INFO,
        duration: int = 3000,
        closable: bool = True,
        position: str = "top-right"
    ):
        super().__init__(parent)
        
        self.parent_widget = parent
        self.message = message
        self.toast_type = toast_type
        self.duration = duration
        self.closable = closable
        self.position = position
        
        # Estado de animación
        self.is_showing = False
        self.is_hiding = False
        
        # Configuración del widget
        self._setup_ui()
        self._setup_animations()
        self._setup_timers()
        self._apply_styles()
        
        # Posicionar el toast
        self._position_toast()
        
        logger.debug(f"Toast creado: {message} ({toast_type.value})")
    
    def _setup_ui(self):
        """Configura la interfaz del toast."""
        # Configuración básica del frame
        self.setFrameStyle(QFrame.Shape.NoFrame)
        
        # No usar altura fija - permitir que se ajuste al contenido
        self.setMinimumSize(300, 50)  # Tamaño mínimo más generoso
        self.setMaximumSize(450, 120)  # Tamaño máximo más amplio
        
        # Layout principal
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)
        
        # Icono del tipo de notificación
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(24, 24)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._set_icon()
        layout.addWidget(self.icon_label)
        
        # Contenido del mensaje
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(2)
        
        # Mensaje principal
        self.message_label = QLabel(self.message)
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.message_label.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding
        )
        font = QFont()
        font.setPointSize(get_fluent_font_size('body'))
        font.setWeight(QFont.Weight.Medium)
        self.message_label.setFont(font)
        content_layout.addWidget(self.message_label)
        
        layout.addLayout(content_layout, 1)  # Expandir
        
        # Botón de cerrar (si es closable)
        if self.closable:
            self.close_button = QPushButton("✕")
            self.close_button.setFixedSize(20, 20)
            self.close_button.setToolTip("Cerrar notificación")
            
            # Conectar tanto hide_toast como force_close para mayor robustez
            self.close_button.clicked.connect(self._handle_close_button)
            layout.addWidget(self.close_button)
        
        # Efecto de sombra
        self._setup_shadow()
        
        # Ajustar tamaño después de configurar todo
        self.adjustSize()
    
    def _set_icon(self):
        """Establece el icono según el tipo de toast."""
        icons = {
            ToastType.SUCCESS: "✓",
            ToastType.ERROR: "✕", 
            ToastType.WARNING: "⚠",
            ToastType.INFO: "ℹ"
        }
        
        icon_text = icons.get(self.toast_type, "ℹ")
        self.icon_label.setText(icon_text)
        
        # Fuente para el icono
        font = QFont()
        font.setPointSize(16)
        font.setWeight(QFont.Weight.Bold)
        self.icon_label.setFont(font)
    
    def _setup_shadow(self):
        """Configura el efecto de sombra."""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 60))  # Sombra sutil
        self.setGraphicsEffect(shadow)
    
    def _setup_animations(self):
        """Configura las animaciones de entrada y salida."""
        # Animación de posición (deslizamiento)
        self.slide_animation = QPropertyAnimation(self, b"pos")
        self.slide_animation.setDuration(300)
        self.slide_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Animación de opacidad
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity") 
        self.fade_animation.setDuration(300)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Grupo de animaciones paralelas
        self.animation_group = QParallelAnimationGroup()
        self.animation_group.addAnimation(self.slide_animation)
        self.animation_group.addAnimation(self.fade_animation)
        
        # Conectar señales
        self.animation_group.finished.connect(self._on_animation_finished)
    
    def _setup_timers(self):
        """Configura los timers para auto-hide."""
        if self.duration > 0:
            self.hide_timer = QTimer()
            self.hide_timer.setSingleShot(True)
            self.hide_timer.timeout.connect(self.hide_toast)
    
    def _apply_styles(self):
        """Aplica los estilos Fluent según el tipo de toast."""
        colors = obtener_fluent_colors()
        
        # Colores según el tipo
        color_schemes = {
            ToastType.SUCCESS: {
                'bg': colors['success'],
                'fg': '#FFFFFF',
                'icon': '#FFFFFF',
                'border': colors['success']
            },
            ToastType.ERROR: {
                'bg': colors['error'],
                'fg': '#FFFFFF', 
                'icon': '#FFFFFF',
                'border': colors['error']
            },
            ToastType.WARNING: {
                'bg': colors['warning'],
                'fg': '#000000',
                'icon': '#000000', 
                'border': colors['warning']
            },
            ToastType.INFO: {
                'bg': colors['primary'],
                'fg': colors['text_on_accent'],
                'icon': colors['text_on_accent'],
                'border': colors['primary']
            }
        }
        
        scheme = color_schemes.get(self.toast_type, color_schemes[ToastType.INFO])
        border_radius = get_fluent_border_radius('medium')
        
        # Estilo del frame principal
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {scheme['bg']};
                border: 1px solid {scheme['border']};
                border-radius: {border_radius}px;
                color: {scheme['fg']};
            }}
        """)
        
        # Estilo del mensaje
        self.message_label.setStyleSheet(f"""
            QLabel {{
                color: {scheme['fg']};
                background: transparent;
                border: none;
            }}
        """)
        
        # Estilo del icono
        self.icon_label.setStyleSheet(f"""
            QLabel {{
                color: {scheme['icon']};
                background: transparent;
                border: none;
                font-weight: bold;
            }}
        """)
        
        # Estilo del botón cerrar (si existe)
        if self.closable:
            self.close_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(255, 255, 255, 0.2);
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    border-radius: 10px;
                    color: {scheme['fg']};
                    font-weight: bold;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: rgba(255, 255, 255, 0.3);
                    border-color: rgba(255, 255, 255, 0.5);
                }}
                QPushButton:pressed {{
                    background-color: rgba(255, 255, 255, 0.1);
                }}
            """)
    
    def _position_toast(self):
        """Posiciona el toast en la ventana padre."""
        if not self.parent_widget:
            return
        
        # Asegurar que el widget esté completamente configurado
        self.adjustSize()  # Ajustar al tamaño del contenido
        
        parent_rect = self.parent_widget.rect()
        toast_size = self.size()
        toast_width = toast_size.width()
        toast_height = toast_size.height()
        
        margin = get_fluent_spacing('xl')  # 20px
        
        # Verificar que el toast no sea más grande que la ventana padre
        if toast_width > parent_rect.width() - (2 * margin):
            toast_width = parent_rect.width() - (2 * margin)
            self.setFixedWidth(toast_width)
        
        if toast_height > parent_rect.height() - (2 * margin):
            toast_height = parent_rect.height() - (2 * margin)
            self.setFixedHeight(toast_height)
        
        # Calcular posición según el tipo
        if self.position == "top-right":
            x = parent_rect.width() - toast_width - margin
            y = margin
        elif self.position == "top-left":
            x = margin
            y = margin
        elif self.position == "bottom-right":
            x = parent_rect.width() - toast_width - margin
            y = parent_rect.height() - toast_height - margin
        elif self.position == "bottom-left":
            x = margin
            y = parent_rect.height() - toast_height - margin
        elif self.position == "center":
            x = (parent_rect.width() - toast_width) // 2
            y = (parent_rect.height() - toast_height) // 2
        else:
            # Default: top-right
            x = parent_rect.width() - toast_width - margin
            y = margin
        
        # Asegurar que el toast esté dentro de los límites visibles
        x = max(0, min(x, parent_rect.width() - toast_width))
        y = max(0, min(y, parent_rect.height() - toast_height))
        
        # Posición inicial (fuera de la pantalla para animación)
        if "right" in self.position:
            start_x = parent_rect.width() + toast_width
        else:
            start_x = -toast_width
        
        self.start_pos = QPoint(start_x, y)
        self.end_pos = QPoint(x, y)
        
        # Establecer posición inicial
        self.move(self.start_pos)
        
        logger.debug(f"Toast posicionado: {toast_width}x{toast_height} en ({x}, {y})")
    
    def show_toast(self):
        """Muestra el toast con animación."""
        if self.is_showing or self.is_hiding:
            return
        
        self.is_showing = True
        self.show()
        
        # Configurar animaciones de entrada
        self.slide_animation.setStartValue(self.start_pos)
        self.slide_animation.setEndValue(self.end_pos)
        
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        
        # Iniciar animación
        self.animation_group.start()
        
        # Iniciar timer de auto-hide
        if hasattr(self, 'hide_timer'):
            self.hide_timer.start(self.duration)
        
        logger.debug(f"Toast mostrado: {self.message}")
    
    def hide_toast(self):
        """Oculta el toast con animación."""
        if self.is_hiding:
            return
        
        # Debug: verificar estado actual
        logger.debug(f"Intentando ocultar toast: {self.message}, is_showing: {self.is_showing}, is_hiding: {self.is_hiding}")
        
        self.is_hiding = True
        self.is_showing = False  # Asegurar que is_showing se establezca correctamente
        
        # Detener timer si está activo
        if hasattr(self, 'hide_timer') and self.hide_timer.isActive():
            self.hide_timer.stop()
        
        # Verificar que las animaciones estén configuradas
        if not hasattr(self, 'animation_group'):
            logger.warning("Animation group no encontrado, cerrando directamente")
            self.close()
            self.closed.emit()
            return
        
        # Configurar animaciones de salida
        self.slide_animation.setStartValue(self.pos())  # Usar posición actual
        self.slide_animation.setEndValue(self.start_pos)
        
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        
        # Iniciar animación de salida
        self.animation_group.start()
        
        logger.debug(f"Toast ocultándose: {self.message}")
    
    def force_close(self):
        """Fuerza el cierre inmediato del toast sin animación."""
        logger.debug(f"Forzando cierre de toast: {self.message}")
        
        # Detener todas las animaciones
        if hasattr(self, 'animation_group'):
            self.animation_group.stop()
        
        # Detener timer
        if hasattr(self, 'hide_timer') and self.hide_timer.isActive():
            self.hide_timer.stop()
        
        # Cerrar inmediatamente
        self.setVisible(False)
        self.close()
        self.closed.emit()
    
    def _handle_close_button(self):
        """Maneja el clic en el botón de cerrar - Versión directa y simple."""
        logger.debug(f"🔵 CLOSE BUTTON CLICKED: {self.message}")
        
        # Cancelar timer de auto-hide
        if hasattr(self, 'hide_timer') and self.hide_timer.isActive():
            self.hide_timer.stop()
            logger.debug("⏹️ Auto-hide timer detenido")
        
        # Cierre inmediato y directo
        self.force_close()
    
    def _check_and_force_close(self):
        """Verifica si el toast se cerró, si no, fuerza el cierre."""
        if self.isVisible():
            logger.debug(f"🔄 Forzando cierre desde check: {self.message}")
            self.force_close()
    
    def _on_animation_finished(self):
        """Maneja el fin de las animaciones."""
        if self.is_hiding:
            # Asegurar que el widget se cierre correctamente
            self.setVisible(False)
            self.close()
            self.closed.emit()
            logger.debug(f"Toast cerrado completamente: {self.message}")
        else:
            # Animación de entrada completada
            self.is_showing = True
            logger.debug(f"Toast mostrado completamente: {self.message}")
    
    def mousePressEvent(self, event):
        """Maneja clics en el toast."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)
    
    def resizeEvent(self, event):
        """Maneja cambios de tamaño del widget."""
        super().resizeEvent(event)
        # Reposicionar si es necesario
        if hasattr(self, 'parent_widget') and self.parent_widget:
            self._position_toast()
    
    def showEvent(self, event):
        """Maneja cuando el widget se muestra."""
        super().showEvent(event)
        # Asegurar posicionamiento correcto al mostrar
        self._position_toast()


class ToastManager:
    """
    Gestor de notificaciones toast para la aplicación.
    
    Maneja múltiples toasts, posicionamiento automático y cola de notificaciones.
    """
    
    def __init__(self, parent_widget: QWidget):
        self.parent_widget = parent_widget
        self.active_toasts = []
        self.toast_queue = []
        self.max_toasts = 5  # Máximo de toasts simultáneos
        
        logger.info("ToastManager inicializado")
    
    def show_success(self, message: str, duration: int = 3000, closable: bool = True):
        """Muestra una notificación de éxito."""
        self._show_toast(message, ToastType.SUCCESS, duration, closable)
    
    def show_error(self, message: str, duration: int = 5000, closable: bool = True):
        """Muestra una notificación de error."""
        self._show_toast(message, ToastType.ERROR, duration, closable)
    
    def show_warning(self, message: str, duration: int = 4000, closable: bool = True):
        """Muestra una notificación de advertencia."""
        self._show_toast(message, ToastType.WARNING, duration, closable)
    
    def show_info(self, message: str, duration: int = 3000, closable: bool = True):
        """Muestra una notificación informativa."""
        self._show_toast(message, ToastType.INFO, duration, closable)
    
    def _show_toast(
        self, 
        message: str, 
        toast_type: ToastType, 
        duration: int, 
        closable: bool
    ):
        """Muestra un toast del tipo especificado."""
        if len(self.active_toasts) >= self.max_toasts:
            # Agregar a la cola
            self.toast_queue.append((message, toast_type, duration, closable))
            return
        
        # Calcular posición (apilado vertical)
        position = self._get_next_position()
        vertical_offset = self._calculate_toast_offset()
        
        toast = ToastNotification(
            parent=self.parent_widget,
            message=message,
            toast_type=toast_type,
            duration=duration,
            closable=closable,
            position=position
        )
        
        # Ajustar posición vertical para apilar
        if vertical_offset > 0:
            original_pos = toast.end_pos
            toast.end_pos = QPoint(original_pos.x(), original_pos.y() + vertical_offset)
            toast.start_pos = QPoint(toast.start_pos.x(), toast.start_pos.y() + vertical_offset)
        
        # Conectar señales
        toast.closed.connect(lambda: self._on_toast_closed(toast))
        
        # Agregar a la lista activa
        self.active_toasts.append(toast)
        
        # Mostrar el toast
        toast.show_toast()
        
        logger.info(f"Toast {toast_type.value}: {message}")
    
    def _get_next_position(self) -> str:
        """Calcula la posición del siguiente toast."""
        # Por ahora, todos en top-right con apilado vertical
        return "top-right"
    
    def _calculate_toast_offset(self) -> int:
        """Calcula el offset vertical para apilar toasts."""
        offset = 0
        spacing = get_fluent_spacing('md')  # 12px entre toasts
        
        for toast in self.active_toasts:
            if toast.isVisible():
                offset += toast.height() + spacing
        
        return offset
    
    def _on_toast_closed(self, toast: ToastNotification):
        """Maneja el cierre de un toast."""
        if toast in self.active_toasts:
            self.active_toasts.remove(toast)
        
        # Procesar cola si hay toasts pendientes
        if self.toast_queue:
            message, toast_type, duration, closable = self.toast_queue.pop(0)
            self._show_toast(message, toast_type, duration, closable)
    
    def clear_all(self):
        """Cierra todos los toasts activos."""
        for toast in self.active_toasts[:]:  # Copia para evitar modificación durante iteración
            toast.hide_toast()
        
        self.toast_queue.clear()
        logger.info("Todos los toasts han sido limpiados")


# Funciones de conveniencia para uso global
_global_toast_manager: Optional[ToastManager] = None

def init_toast_system(parent_widget: QWidget):
    """Inicializa el sistema global de toasts."""
    global _global_toast_manager
    _global_toast_manager = ToastManager(parent_widget)
    logger.info("Sistema global de toasts inicializado")

def show_success_toast(message: str, duration: int = 3000):
    """Función global para mostrar toast de éxito."""
    if _global_toast_manager:
        _global_toast_manager.show_success(message, duration)

def show_error_toast(message: str, duration: int = 5000):
    """Función global para mostrar toast de error."""
    if _global_toast_manager:
        _global_toast_manager.show_error(message, duration)

def show_warning_toast(message: str, duration: int = 4000):
    """Función global para mostrar toast de advertencia."""
    if _global_toast_manager:
        _global_toast_manager.show_warning(message, duration)

def show_info_toast(message: str, duration: int = 3000):
    """Función global para mostrar toast informativo."""
    if _global_toast_manager:
        _global_toast_manager.show_info(message, duration)