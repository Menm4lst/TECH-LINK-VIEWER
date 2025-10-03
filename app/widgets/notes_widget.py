#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Widget de Notas para TECH LINK VIEWER 4.0
Sistema de notas integrado con funcionalidades avanzadas
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit,
    QPushButton, QListWidget, QListWidgetItem, QSplitter,
    QLabel, QMessageBox, QInputDialog, QMenu, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QTextCharFormat, QColor, QAction

from ..theme import Colors, Fonts, get_icon
from ..utils.io import cargar_json, guardar_json

logger = logging.getLogger(__name__)


class NotesWidget(QWidget):
    """Widget principal para el sistema de notas"""
    
    # Señales
    nota_guardada = pyqtSignal(str)  # Emite cuando se guarda una nota
    nota_eliminada = pyqtSignal(str)  # Emite cuando se elimina una nota
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.notas_archivo = Path("data/notas.json")
        self.notas_data = {}
        self.nota_actual = None
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self._auto_guardar)
        self.auto_save_timer.setSingleShot(True)
        
        self._setup_ui()
        self._aplicar_estilos()
        self._conectar_eventos()
        self._cargar_notas()
        
        logger.info("Widget de notas inicializado")
    
    def _setup_ui(self):
        """Configura la interfaz del widget"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # Splitter principal
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Panel izquierdo - Lista de notas
        self._crear_panel_notas(splitter)
        
        # Panel derecho - Editor de notas
        self._crear_panel_editor(splitter)
        
        # Configurar proporciones
        splitter.setSizes([300, 700])
        layout.addWidget(splitter)
    
    def _crear_panel_notas(self, splitter):
        """Crea el panel de lista de notas"""
        widget_notas = QWidget()
        layout = QVBoxLayout(widget_notas)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(6)
        
        # Header con título
        header_layout = QHBoxLayout()
        
        label_notas = QLabel("📝 MIS NOTAS")
        label_notas.setFont(Fonts.get_monospace_font(Fonts.SIZE_MEDIUM, bold=True))
        label_notas.setStyleSheet(f"color: {Colors.ACCENT_CYAN}; padding: 8px;")
        
        # Botón nueva nota
        self.btn_nueva_nota = QPushButton()
        self.btn_nueva_nota.setIcon(get_icon('add'))
        self.btn_nueva_nota.setToolTip("Nueva nota (Ctrl+N)")
        self.btn_nueva_nota.setMaximumSize(32, 32)
        
        header_layout.addWidget(label_notas)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_nueva_nota)
        layout.addLayout(header_layout)
        
        # Barra de búsqueda de notas
        self.campo_buscar_notas = QLineEdit()
        self.campo_buscar_notas.setPlaceholderText("🔍 Buscar en notas...")
        self.campo_buscar_notas.setMaximumHeight(32)
        layout.addWidget(self.campo_buscar_notas)
        
        # Lista de notas
        self.lista_notas = QListWidget()
        self.lista_notas.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        layout.addWidget(self.lista_notas)
        
        # Información de estadísticas
        self.label_stats = QLabel("0 notas")
        self.label_stats.setFont(Fonts.get_monospace_font(Fonts.SIZE_SMALL))
        self.label_stats.setStyleSheet(f"color: {Colors.FG_DIM}; padding: 4px;")
        layout.addWidget(self.label_stats)
        
        splitter.addWidget(widget_notas)
    
    def _crear_panel_editor(self, splitter):
        """Crea el panel editor de notas"""
        widget_editor = QWidget()
        layout = QVBoxLayout(widget_editor)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(6)
        
        # Header del editor
        header_layout = QHBoxLayout()
        
        # Campo título de nota
        self.campo_titulo = QLineEdit()
        self.campo_titulo.setPlaceholderText("📝 Título de la nota...")
        self.campo_titulo.setFont(Fonts.get_monospace_font(Fonts.SIZE_MEDIUM, bold=True))
        
        # Botones de acción
        self.btn_guardar = QPushButton()
        self.btn_guardar.setIcon(get_icon('export'))
        self.btn_guardar.setText("Guardar")
        self.btn_guardar.setToolTip("Guardar nota (Ctrl+S)")
        
        self.btn_eliminar = QPushButton()
        self.btn_eliminar.setIcon(get_icon('delete'))
        self.btn_eliminar.setText("Eliminar")
        self.btn_eliminar.setToolTip("Eliminar nota")
        self.btn_eliminar.setEnabled(False)
        
        header_layout.addWidget(self.campo_titulo)
        header_layout.addWidget(self.btn_guardar)
        header_layout.addWidget(self.btn_eliminar)
        layout.addLayout(header_layout)
        
        # Editor de texto
        self.editor_texto = QTextEdit()
        self.editor_texto.setPlaceholderText(
            "✍️ Escribe tus notas aquí...\n\n"
            "💡 Consejos:\n"
            "• Auto-guardado cada 3 segundos\n"
            "• Usa Ctrl+S para guardar manualmente\n"
            "• Ctrl+N para nueva nota\n"
            "• Busca en tus notas con la barra superior"
        )
        self.editor_texto.setFont(Fonts.get_monospace_font(Fonts.SIZE_SMALL))
        layout.addWidget(self.editor_texto)
        
        # Barra de estado del editor
        status_layout = QHBoxLayout()
        
        self.label_auto_save = QLabel("💾 Auto-guardado activo")
        self.label_auto_save.setFont(Fonts.get_monospace_font(Fonts.SIZE_SMALL))
        self.label_auto_save.setStyleSheet(f"color: {Colors.ACCENT_NEO};")
        
        self.label_fecha = QLabel()
        self.label_fecha.setFont(Fonts.get_monospace_font(Fonts.SIZE_SMALL))
        self.label_fecha.setStyleSheet(f"color: {Colors.FG_DIM};")
        
        status_layout.addWidget(self.label_auto_save)
        status_layout.addStretch()
        status_layout.addWidget(self.label_fecha)
        layout.addLayout(status_layout)
        
        splitter.addWidget(widget_editor)
    
    def _aplicar_estilos(self):
        """Aplica estilos del tema oscuro"""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {Colors.BG0};
                color: {Colors.FG};
            }}
            
            QLineEdit {{
                background-color: {Colors.BG1};
                border: 1px solid {Colors.FG_DIM};
                border-radius: 4px;
                padding: 6px;
                color: {Colors.FG};
                font-family: 'Consolas', 'Monaco', monospace;
            }}
            
            QLineEdit:focus {{
                border-color: {Colors.ACCENT_CYAN};
            }}
            
            QTextEdit {{
                background-color: {Colors.BG1};
                border: 1px solid {Colors.FG_DIM};
                border-radius: 4px;
                padding: 8px;
                color: {Colors.FG};
                font-family: 'Consolas', 'Monaco', monospace;
                line-height: 1.4;
            }}
            
            QTextEdit:focus {{
                border-color: {Colors.ACCENT_CYAN};
            }}
            
            QListWidget {{
                background-color: {Colors.BG1};
                border: 1px solid {Colors.FG_DIM};
                border-radius: 4px;
                padding: 4px;
                color: {Colors.FG};
                font-family: 'Consolas', 'Monaco', monospace;
            }}
            
            QListWidget::item {{
                padding: 8px;
                border-radius: 4px;
                margin: 2px;
            }}
            
            QListWidget::item:selected {{
                background-color: {Colors.ACCENT_CYAN};
                color: {Colors.BG0};
            }}
            
            QListWidget::item:hover {{
                background-color: {Colors.BG2};
            }}
            
            QPushButton {{
                background-color: {Colors.BG2};
                border: 1px solid {Colors.FG_DIM};
                border-radius: 4px;
                padding: 6px 12px;
                color: {Colors.FG};
                font-family: 'Consolas', 'Monaco', monospace;
            }}
            
            QPushButton:hover {{
                background-color: {Colors.ACCENT_NEO};
                color: {Colors.BG0};
                border-color: {Colors.ACCENT_NEO};
            }}
            
            QPushButton:pressed {{
                background-color: {Colors.ACCENT_CYAN};
            }}
            
            QPushButton:disabled {{
                background-color: {Colors.BG1};
                color: {Colors.FG_DIM};
                border-color: {Colors.FG_DIM};
            }}
        """)
    
    def _conectar_eventos(self):
        """Conecta las señales de los widgets"""
        # Botones
        self.btn_nueva_nota.clicked.connect(self._nueva_nota)
        self.btn_guardar.clicked.connect(self._guardar_nota_actual)
        self.btn_eliminar.clicked.connect(self._eliminar_nota_actual)
        
        # Lista de notas
        self.lista_notas.itemClicked.connect(self._nota_seleccionada)
        self.lista_notas.customContextMenuRequested.connect(self._mostrar_menu_contexto)
        
        # Editor
        self.editor_texto.textChanged.connect(self._texto_cambiado)
        self.campo_titulo.textChanged.connect(self._titulo_cambiado)
        
        # Búsqueda
        self.campo_buscar_notas.textChanged.connect(self._filtrar_notas)
    
    def _cargar_notas(self):
        """Carga las notas desde el archivo JSON"""
        try:
            if self.notas_archivo.exists():
                self.notas_data = cargar_json(self.notas_archivo)
            else:
                self.notas_data = {}
                # Crear nota de bienvenida
                self._crear_nota_bienvenida()
            
            self._actualizar_lista_notas()
            logger.info(f"Cargadas {len(self.notas_data)} notas")
            
        except Exception as e:
            logger.error(f"Error cargando notas: {e}")
            QMessageBox.warning(self, "Error", f"Error cargando notas: {e}")
            self.notas_data = {}
    
    def _crear_nota_bienvenida(self):
        """Crea una nota de bienvenida para nuevos usuarios"""
        bienvenida_id = f"bienvenida_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.notas_data[bienvenida_id] = {
            "titulo": "🎉 Bienvenido al Sistema de Notas",
            "contenido": """¡Hola! Bienvenido al sistema de notas integrado de TECH LINK VIEWER 4.0.

🚀 CARACTERÍSTICAS PRINCIPALES:
• Auto-guardado inteligente cada 3 segundos
• Búsqueda instantánea en todas tus notas
• Interfaz terminal con tema oscuro
• Menú contextual con opciones avanzadas

⌨️ ATAJOS ÚTILES:
• Ctrl+N: Nueva nota
• Ctrl+S: Guardar nota
• Ctrl+F: Buscar en notas

💡 CONSEJOS:
• Usa títulos descriptivos para encontrar notas fácilmente
• El sistema guarda automáticamente mientras escribes
• Puedes tener múltiples notas abiertas
• Las notas se sincronizan con tus enlaces

📝 CASOS DE USO:
• Documentar APIs y configuraciones
• Guardar snippets de código
• Tomar notas de reuniones
• Planificar proyectos
• Recordatorios y tareas

¡Comienza a escribir y organiza tu trabajo de manera eficiente!

---
Desarrollado por Antware con ❤️ y ☕""",
            "fecha_creacion": datetime.now().isoformat(),
            "fecha_modificacion": datetime.now().isoformat(),
            "tags": ["bienvenida", "tutorial"]
        }
        self._guardar_notas()
    
    def _actualizar_lista_notas(self):
        """Actualiza la lista de notas en la interfaz"""
        self.lista_notas.clear()
        
        # Filtro de búsqueda
        filtro = self.campo_buscar_notas.text().lower()
        
        # Ordenar por fecha de modificación (más reciente primero)
        notas_ordenadas = sorted(
            self.notas_data.items(),
            key=lambda x: x[1].get('fecha_modificacion', ''),
            reverse=True
        )
        
        notas_mostradas = 0
        for nota_id, nota_data in notas_ordenadas:
            titulo = nota_data.get('titulo', 'Sin título')
            contenido = nota_data.get('contenido', '')
            
            # Aplicar filtro
            if filtro and filtro not in titulo.lower() and filtro not in contenido.lower():
                continue
            
            # Crear item de lista
            item = QListWidgetItem()
            
            # Formato del item
            fecha_mod = nota_data.get('fecha_modificacion', '')
            if fecha_mod:
                try:
                    fecha_obj = datetime.fromisoformat(fecha_mod.replace('Z', '+00:00'))
                    fecha_str = fecha_obj.strftime('%d/%m %H:%M')
                except:
                    fecha_str = ''
            else:
                fecha_str = ''
            
            # Texto del item
            item_text = f"{titulo}"
            if fecha_str:
                item_text += f"\n📅 {fecha_str}"
            
            # Preview del contenido
            preview = contenido[:100].replace('\n', ' ')
            if len(contenido) > 100:
                preview += "..."
            if preview:
                item_text += f"\n💬 {preview}"
            
            item.setText(item_text)
            item.setData(Qt.ItemDataRole.UserRole, nota_id)
            
            self.lista_notas.addItem(item)
            notas_mostradas += 1
        
        # Actualizar estadísticas
        total_notas = len(self.notas_data)
        if filtro:
            self.label_stats.setText(f"{notas_mostradas} de {total_notas} notas")
        else:
            self.label_stats.setText(f"{total_notas} notas")
    
    def _nueva_nota(self):
        """Crea una nueva nota"""
        # Pedir título
        titulo, ok = QInputDialog.getText(
            self, 
            "Nueva Nota", 
            "Título de la nota:",
            text="Mi nueva nota"
        )
        
        if not ok or not titulo.strip():
            return
        
        # Generar ID único
        nota_id = f"nota_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Crear nota
        self.notas_data[nota_id] = {
            "titulo": titulo.strip(),
            "contenido": "",
            "fecha_creacion": datetime.now().isoformat(),
            "fecha_modificacion": datetime.now().isoformat(),
            "tags": []
        }
        
        # Guardar y actualizar
        self._guardar_notas()
        self._actualizar_lista_notas()
        
        # Seleccionar la nueva nota
        for i in range(self.lista_notas.count()):
            item = self.lista_notas.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == nota_id:
                self.lista_notas.setCurrentItem(item)
                self._nota_seleccionada(item)
                break
        
        # Enfocar el editor
        self.editor_texto.setFocus()
        
        logger.info(f"Nueva nota creada: {titulo}")
    
    def _nota_seleccionada(self, item):
        """Maneja la selección de una nota"""
        if not item:
            return
        
        nota_id = item.data(Qt.ItemDataRole.UserRole)
        if nota_id not in self.notas_data:
            return
        
        self.nota_actual = nota_id
        nota_data = self.notas_data[nota_id]
        
        # Cargar datos en el editor
        self.campo_titulo.setText(nota_data.get('titulo', ''))
        self.editor_texto.setText(nota_data.get('contenido', ''))
        
        # Actualizar fecha
        fecha_mod = nota_data.get('fecha_modificacion', '')
        if fecha_mod:
            try:
                fecha_obj = datetime.fromisoformat(fecha_mod.replace('Z', '+00:00'))
                fecha_str = fecha_obj.strftime('%d/%m/%Y %H:%M')
                self.label_fecha.setText(f"📅 Modificado: {fecha_str}")
            except:
                self.label_fecha.setText("")
        else:
            self.label_fecha.setText("")
        
        # Habilitar botón eliminar
        self.btn_eliminar.setEnabled(True)
        
        logger.debug(f"Nota seleccionada: {nota_data.get('titulo', nota_id)}")
    
    def _texto_cambiado(self):
        """Maneja cambios en el editor de texto"""
        if self.nota_actual:
            # Reiniciar timer de auto-guardado
            self.auto_save_timer.start(3000)  # 3 segundos
    
    def _titulo_cambiado(self):
        """Maneja cambios en el título"""
        if self.nota_actual:
            self.auto_save_timer.start(3000)
    
    def _auto_guardar(self):
        """Guarda automáticamente la nota actual"""
        if self.nota_actual and self.nota_actual in self.notas_data:
            self.notas_data[self.nota_actual]["titulo"] = self.campo_titulo.text().strip()
            self.notas_data[self.nota_actual]["contenido"] = self.editor_texto.toPlainText()
            self.notas_data[self.nota_actual]["fecha_modificacion"] = datetime.now().isoformat()
            
            self._guardar_notas()
            self._actualizar_lista_notas()
            
            # Actualizar indicador
            self.label_auto_save.setText("💾 Guardado automáticamente")
            QTimer.singleShot(2000, lambda: self.label_auto_save.setText("💾 Auto-guardado activo"))
    
    def _guardar_nota_actual(self):
        """Guarda manualmente la nota actual"""
        if not self.nota_actual:
            return
        
        if self.nota_actual in self.notas_data:
            self.notas_data[self.nota_actual]["titulo"] = self.campo_titulo.text().strip()
            self.notas_data[self.nota_actual]["contenido"] = self.editor_texto.toPlainText()
            self.notas_data[self.nota_actual]["fecha_modificacion"] = datetime.now().isoformat()
            
            self._guardar_notas()
            self._actualizar_lista_notas()
            
            self.label_auto_save.setText("💾 Guardado manualmente")
            QTimer.singleShot(2000, lambda: self.label_auto_save.setText("💾 Auto-guardado activo"))
            
            self.nota_guardada.emit(self.nota_actual)
            logger.info(f"Nota guardada manualmente: {self.campo_titulo.text()}")
    
    def _eliminar_nota_actual(self):
        """Elimina la nota actual"""
        if not self.nota_actual or self.nota_actual not in self.notas_data:
            return
        
        titulo = self.notas_data[self.nota_actual].get('titulo', 'Sin título')
        
        respuesta = QMessageBox.question(
            self,
            "Eliminar Nota",
            f"¿Estás seguro de que quieres eliminar la nota '{titulo}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            del self.notas_data[self.nota_actual]
            self._guardar_notas()
            self._actualizar_lista_notas()
            
            # Limpiar editor
            self.campo_titulo.clear()
            self.editor_texto.clear()
            self.label_fecha.clear()
            self.btn_eliminar.setEnabled(False)
            self.nota_actual = None
            
            self.nota_eliminada.emit(titulo)
            logger.info(f"Nota eliminada: {titulo}")
    
    def _filtrar_notas(self):
        """Filtra las notas según el texto de búsqueda"""
        self._actualizar_lista_notas()
    
    def _mostrar_menu_contexto(self, position):
        """Muestra el menú contextual de la lista de notas"""
        item = self.lista_notas.itemAt(position)
        if not item:
            return
        
        menu = QMenu(self)
        
        # Acción abrir
        accion_abrir = QAction("📖 Abrir", self)
        accion_abrir.triggered.connect(lambda: self._nota_seleccionada(item))
        menu.addAction(accion_abrir)
        
        menu.addSeparator()
        
        # Acción duplicar
        accion_duplicar = QAction("📋 Duplicar", self)
        accion_duplicar.triggered.connect(lambda: self._duplicar_nota(item))
        menu.addAction(accion_duplicar)
        
        # Acción eliminar
        accion_eliminar = QAction("🗑️ Eliminar", self)
        accion_eliminar.triggered.connect(lambda: self._eliminar_nota_item(item))
        menu.addAction(accion_eliminar)
        
        menu.exec(self.lista_notas.mapToGlobal(position))
    
    def _duplicar_nota(self, item):
        """Duplica una nota"""
        nota_id = item.data(Qt.ItemDataRole.UserRole)
        if nota_id not in self.notas_data:
            return
        
        nota_original = self.notas_data[nota_id]
        nuevo_id = f"nota_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.notas_data[nuevo_id] = {
            "titulo": f"{nota_original['titulo']} (Copia)",
            "contenido": nota_original['contenido'],
            "fecha_creacion": datetime.now().isoformat(),
            "fecha_modificacion": datetime.now().isoformat(),
            "tags": nota_original.get('tags', []).copy()
        }
        
        self._guardar_notas()
        self._actualizar_lista_notas()
        
        logger.info(f"Nota duplicada: {nota_original['titulo']}")
    
    def _eliminar_nota_item(self, item):
        """Elimina una nota específica"""
        nota_id = item.data(Qt.ItemDataRole.UserRole)
        if nota_id not in self.notas_data:
            return
        
        titulo = self.notas_data[nota_id].get('titulo', 'Sin título')
        
        respuesta = QMessageBox.question(
            self,
            "Eliminar Nota",
            f"¿Estás seguro de que quieres eliminar la nota '{titulo}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            del self.notas_data[nota_id]
            self._guardar_notas()
            self._actualizar_lista_notas()
            
            # Si era la nota actual, limpiar editor
            if self.nota_actual == nota_id:
                self.campo_titulo.clear()
                self.editor_texto.clear()
                self.label_fecha.clear()
                self.btn_eliminar.setEnabled(False)
                self.nota_actual = None
            
            self.nota_eliminada.emit(titulo)
            logger.info(f"Nota eliminada: {titulo}")
    
    def _guardar_notas(self):
        """Guarda las notas en el archivo JSON"""
        try:
            # Asegurar que el directorio existe
            self.notas_archivo.parent.mkdir(exist_ok=True)
            
            # Guardar con formato legible
            guardar_json(self.notas_data, self.notas_archivo)
            
        except Exception as e:
            logger.error(f"Error guardando notas: {e}")
            QMessageBox.warning(self, "Error", f"Error guardando notas: {e}")
    
    def obtener_estadisticas(self) -> Dict:
        """Retorna estadísticas de las notas"""
        total_notas = len(self.notas_data)
        total_caracteres = sum(len(nota.get('contenido', '')) for nota in self.notas_data.values())
        
        return {
            "total_notas": total_notas,
            "total_caracteres": total_caracteres,
            "promedio_caracteres": total_caracteres // total_notas if total_notas > 0 else 0
        }
    
    def buscar_en_notas(self, termino: str) -> List[Dict]:
        """Busca un término en todas las notas"""
        resultados = []
        termino_lower = termino.lower()
        
        for nota_id, nota_data in self.notas_data.items():
            titulo = nota_data.get('titulo', '')
            contenido = nota_data.get('contenido', '')
            
            if termino_lower in titulo.lower() or termino_lower in contenido.lower():
                resultados.append({
                    "id": nota_id,
                    "titulo": titulo,
                    "coincidencia_titulo": termino_lower in titulo.lower(),
                    "coincidencia_contenido": termino_lower in contenido.lower()
                })
        
        return resultados