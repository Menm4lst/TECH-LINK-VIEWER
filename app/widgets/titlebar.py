#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Widget de título con efecto typewriter para TECH LINK VIEWER
Header con animación de tipeo y borrado estilo terminal/consola
"""

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import QTimer, pyqtSignal, Qt
from PyQt6.QtGui import QFont, QPalette
from ..theme.colors import Colors
from ..theme.fonts import Fonts

class TitleBar(QWidget):
    """
    Barra de título con efecto typewriter animado
    Muestra TECH LINK VIEWER con caret parpadeando estilo terminal
    """
    
    # Señales
    animation_finished = pyqtSignal()
    text_completed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Configuración de la animación
        self.full_text = "TECH LINK VIEWER"
        self.subtitle = "Global link search • JSON • PyQt6"
        self.current_text = ""
        self.current_index = 0
        self.is_typing = True
        self.is_erasing = False
        self.show_caret = True
        
        # Configuración personalizable
        self.type_speed = 120  # ms entre caracteres al escribir
        self.erase_speed = 80  # ms entre caracteres al borrar
        self.pause_duration = 2000  # ms de pausa con texto completo
        self.erase_pause = 500  # ms de pausa antes de empezar a borrar
        self.caret_blink_speed = 500  # ms para parpadeo del caret
        self.caret_char = "█"  # Carácter del caret
        self.loop_enabled = True  # Si hacer loop automático
        
        # Estado interno
        self._is_running = False
        self._pause_timer = None
        
        self._setup_ui()
        self._setup_timers()
        self._apply_styles()
    
    def _setup_ui(self):
        """Configura la interfaz del widget"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 2)
        layout.setSpacing(1)
        
        # Header container
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        
        # Label principal con el texto animado
        self.title_label = QLabel()
        self.title_label.setFont(Fonts.get_monospace_font(Fonts.SIZE_LARGE, bold=True))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        # Label del subtítulo
        self.subtitle_label = QLabel(self.subtitle)
        self.subtitle_label.setFont(Fonts.get_monospace_font(Fonts.SIZE_SMALL))
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        # Agregar a layouts
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        layout.addWidget(self.subtitle_label)
        
        self.setLayout(layout)
    
    def _setup_timers(self):
        """Configura los timers para la animación"""
        # Timer principal para typewriter
        self.typewriter_timer = QTimer()
        self.typewriter_timer.timeout.connect(self._update_text)
        
        # Timer para parpadeo del caret
        self.caret_timer = QTimer()
        self.caret_timer.timeout.connect(self._toggle_caret)
        
    def _apply_styles(self):
        """Aplica los estilos del tema oscuro"""
        self.setStyleSheet(f"""
        TitleBar {{
            background-color: {Colors.BG1};
            border-bottom: 1px solid {Colors.BORDER};
            border-radius: 0px;
        }}
        
        QLabel {{
            background-color: transparent;
            border: none;
        }}
        """)
        
        # Estilos específicos para labels
        self.title_label.setStyleSheet(f"""
        QLabel {{
            color: {Colors.FG};
            font-weight: bold;
            letter-spacing: 1px;
        }}
        """)
        
        self.subtitle_label.setStyleSheet(f"""
        QLabel {{
            color: {Colors.FG_DIM};
            font-weight: normal;
        }}
        """)
    
    def _update_text(self):
        """Actualiza el texto en cada tick del timer"""
        if self.is_typing:
            # Modo escritura
            if self.current_index < len(self.full_text):
                self.current_text += self.full_text[self.current_index]
                self.current_index += 1
                self._update_display()
            else:
                # Texto completo, iniciar pausa
                self.is_typing = False
                self.typewriter_timer.stop()
                self.text_completed.emit(self.current_text)
                
                if self.loop_enabled:
                    # Programar inicio de borrado después de la pausa
                    self._pause_timer = QTimer()
                    self._pause_timer.setSingleShot(True)
                    self._pause_timer.timeout.connect(self._start_erasing)
                    self._pause_timer.start(self.pause_duration)
        
        elif self.is_erasing:
            # Modo borrado
            if len(self.current_text) > 0:
                self.current_text = self.current_text[:-1]
                self.current_index -= 1
                self._update_display()
            else:
                # Texto borrado completamente, reiniciar
                self.is_erasing = False
                self.typewriter_timer.stop()
                
                if self.loop_enabled:
                    # Breve pausa antes de empezar de nuevo
                    self._pause_timer = QTimer()
                    self._pause_timer.setSingleShot(True)
                    self._pause_timer.timeout.connect(self._restart_typing)
                    self._pause_timer.start(self.erase_pause)
                else:
                    self.animation_finished.emit()
    
    def _update_display(self):
        """Actualiza el display con el texto actual y caret"""
        display_text = self.current_text
        if self.show_caret:
            display_text += f'<span style="color: {Colors.ACCENT_NEO};">{self.caret_char}</span>'
        
        self.title_label.setText(display_text)
    
    def _toggle_caret(self):
        """Alterna la visibilidad del caret"""
        self.show_caret = not self.show_caret
        self._update_display()
    
    def _start_erasing(self):
        """Inicia el modo de borrado"""
        self.is_erasing = True
        self.typewriter_timer.start(self.erase_speed)
    
    def _restart_typing(self):
        """Reinicia la animación de tipeo"""
        self.current_text = ""
        self.current_index = 0
        self.is_typing = True
        self.is_erasing = False
        self.typewriter_timer.start(self.type_speed)
    
    def start(self):
        """Inicia la animación typewriter"""
        if self._is_running:
            return
        
        self._is_running = True
        self.current_text = ""
        self.current_index = 0
        self.is_typing = True
        self.is_erasing = False
        self.show_caret = True
        
        # Iniciar timers
        self.typewriter_timer.start(self.type_speed)
        self.caret_timer.start(self.caret_blink_speed)
    
    def stop(self):
        """Detiene la animación typewriter"""
        self._is_running = False
        
        # Detener timers
        self.typewriter_timer.stop()
        self.caret_timer.stop()
        
        if self._pause_timer:
            self._pause_timer.stop()
            self._pause_timer = None
        
        # Mostrar texto completo sin caret
        self.show_caret = False
        self.current_text = self.full_text
        self._update_display()
    
    def pause(self):
        """Pausa la animación"""
        self.typewriter_timer.stop()
        if self._pause_timer:
            self._pause_timer.stop()
    
    def resume(self):
        """Reanuda la animación"""
        if self._is_running:
            if self.is_typing or self.is_erasing:
                speed = self.type_speed if self.is_typing else self.erase_speed
                self.typewriter_timer.start(speed)
    
    def set_text(self, text: str):
        """Cambia el texto a animar"""
        self.full_text = text
        if not self._is_running:
            self.current_text = text
            self._update_display()
    
    def set_subtitle(self, subtitle: str):
        """Cambia el subtítulo"""
        self.subtitle = subtitle
        self.subtitle_label.setText(subtitle)
    
    def configure(self, **kwargs):
        """
        Configura parámetros de la animación
        
        Parámetros disponibles:
        - type_speed: velocidad de tipeo (ms)
        - erase_speed: velocidad de borrado (ms)
        - pause_duration: pausa con texto completo (ms)
        - erase_pause: pausa antes de borrar (ms)
        - caret_blink_speed: velocidad de parpadeo (ms)
        - caret_char: carácter del caret
        - loop_enabled: si hacer loop automático
        """
        if 'type_speed' in kwargs:
            self.type_speed = kwargs['type_speed']
        
        if 'erase_speed' in kwargs:
            self.erase_speed = kwargs['erase_speed']
        
        if 'pause_duration' in kwargs:
            self.pause_duration = kwargs['pause_duration']
        
        if 'erase_pause' in kwargs:
            self.erase_pause = kwargs['erase_pause']
        
        if 'caret_blink_speed' in kwargs:
            self.caret_blink_speed = kwargs['caret_blink_speed']
            if self._is_running:
                self.caret_timer.start(self.caret_blink_speed)
        
        if 'caret_char' in kwargs:
            self.caret_char = kwargs['caret_char']
        
        if 'loop_enabled' in kwargs:
            self.loop_enabled = kwargs['loop_enabled']
    
    def is_running(self) -> bool:
        """Retorna si la animación está corriendo"""
        return self._is_running
    
    def get_current_text(self) -> str:
        """Retorna el texto actual (sin caret)"""
        return self.current_text
    
    def get_config(self) -> dict:
        """Retorna la configuración actual"""
        return {
            'type_speed': self.type_speed,
            'erase_speed': self.erase_speed,
            'pause_duration': self.pause_duration,
            'erase_pause': self.erase_pause,
            'caret_blink_speed': self.caret_blink_speed,
            'caret_char': self.caret_char,
            'loop_enabled': self.loop_enabled,
            'full_text': self.full_text,
            'subtitle': self.subtitle
        }