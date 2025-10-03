"""
Diálogo para crear y editar enlaces.
"""
from typing import Optional, List, Dict, Any
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLineEdit, QTextEdit, QComboBox, QPushButton, 
    QLabel, QMessageBox, QCompleter
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from ..utils.validators import validar_url, validar_titulo, validar_categoria, limpiar_url
from ..theme.apply import apply_dark_theme
from ..theme.fonts import Fonts


class DialogoEnlace(QDialog):
    """
    Diálogo para crear o editar un enlace.
    """
    
    # Señal emitida cuando se acepta el diálogo con datos válidos
    enlace_aceptado = pyqtSignal(dict)
    
    def __init__(self, parent=None, enlace_existente: Optional[Dict[str, Any]] = None,
                 categorias_existentes: Optional[List[str]] = None,
                 tags_existentes: Optional[List[str]] = None):
        super().__init__(parent)
        self._enlace_existente = enlace_existente
        self._categorias_existentes = categorias_existentes or []
        self._tags_existentes = tags_existentes or []
        self._es_edicion = enlace_existente is not None
        
        self._configurar_dialogo()
        self._crear_interfaz()
        self._configurar_validaciones()
        self._cargar_datos_existentes()
        self._conectar_senales()
    
    def _configurar_dialogo(self) -> None:
        """Configura las propiedades básicas del diálogo."""
        titulo = "Editar Enlace" if self._es_edicion else "Nuevo Enlace"
        self.setWindowTitle(f"🔗 {titulo}")
        self.setModal(True)
        self.setMinimumSize(500, 400)
        self.setMaximumSize(700, 600)
        
        # Configurar fuente del nuevo sistema de tema
        fuente = Fonts.get_monospace_font(size=10)
        self.setFont(fuente)
        
        # Aplicar nuevo tema oscuro
        from PyQt6.QtWidgets import QApplication
        apply_dark_theme(QApplication.instance())
    
    def _crear_interfaz(self) -> None:
        layout_principal = QVBoxLayout(self)
        layout_principal.setSpacing(15)
        
        titulo = "Editar Enlace" if self._es_edicion else "Crear Nuevo Enlace"
        label_titulo = QLabel(titulo)
        fuente_titulo = QFont()
        fuente_titulo.setPointSize(14)
        fuente_titulo.setBold(True)
        label_titulo.setFont(fuente_titulo)
        label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(label_titulo)
        
        self._crear_formulario(layout_principal)
        self._crear_botones(layout_principal)
    
    def _crear_formulario(self, layout_padre: QVBoxLayout) -> None:
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # Campo título
        self.campo_titulo = QLineEdit()
        self.campo_titulo.setMaxLength(200)
        self.campo_titulo.setPlaceholderText("Ingresa el título del enlace...")
        form_layout.addRow("Título *:", self.campo_titulo)
        
        # Campo URL
        self.campo_url = QLineEdit()
        self.campo_url.setMaxLength(500)
        self.campo_url.setPlaceholderText("https://ejemplo.com")
        form_layout.addRow("URL *:", self.campo_url)
        
        # Campo categoría
        self.campo_categoria = QComboBox()
        self.campo_categoria.setEditable(True)
        self.campo_categoria.setMaxCount(100)
        self.campo_categoria.addItems(self._categorias_existentes)
        self.campo_categoria.setCurrentText("")
        self.campo_categoria.lineEdit().setPlaceholderText("Selecciona o ingresa categoría...")
        
        if self._categorias_existentes:
            completador_categoria = QCompleter(self._categorias_existentes)
            completador_categoria.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            self.campo_categoria.setCompleter(completador_categoria)
        
        form_layout.addRow("Categoría *:", self.campo_categoria)
        
        # Campo tags
        self.campo_tags = QTextEdit()
        self.campo_tags.setMaximumHeight(80)
        self.campo_tags.setPlaceholderText("Ingresa tags separados por comas: tag1, tag2, tag3...")
        
        texto_ayuda = "💡 Separa los tags con comas."
        if self._tags_existentes:
            sugerencias = ', '.join(self._tags_existentes[:5])
            texto_ayuda += f" Sugerencias: {sugerencias}"
        
        label_ayuda_tags = QLabel(texto_ayuda)
        label_ayuda_tags.setStyleSheet("color: gray; font-size: 9px;")
        label_ayuda_tags.setWordWrap(True)
        
        form_layout.addRow("Tags:", self.campo_tags)
        form_layout.addRow("", label_ayuda_tags)
        
        # Información adicional para edición
        if self._es_edicion:
            info_layout = QVBoxLayout()
            
            id_enlace = self._enlace_existente.get('id', 'No disponible')
            label_id = QLabel(f"ID: {id_enlace}")
            label_id.setStyleSheet("color: gray; font-size: 9px;")
            info_layout.addWidget(label_id)
            
            from ..utils.time import formatear_fecha
            creado_en = self._enlace_existente.get('creado_en', '')
            actualizado_en = self._enlace_existente.get('actualizado_en', '')
            
            if creado_en:
                label_creado = QLabel(f"Creado: {formatear_fecha(creado_en)}")
                label_creado.setStyleSheet("color: gray; font-size: 9px;")
                info_layout.addWidget(label_creado)
            
            if actualizado_en:
                label_actualizado = QLabel(f"Actualizado: {formatear_fecha(actualizado_en)}")
                label_actualizado.setStyleSheet("color: gray; font-size: 9px;")
                info_layout.addWidget(label_actualizado)
            
            form_layout.addRow("Información:", info_layout)
        
        layout_padre.addLayout(form_layout)
    
    def _crear_botones(self, layout_padre: QVBoxLayout) -> None:
        layout_botones = QHBoxLayout()
        
        self.boton_cancelar = QPushButton("Cancelar")
        self.boton_cancelar.setMinimumWidth(100)
        layout_botones.addWidget(self.boton_cancelar)
        
        layout_botones.addStretch()
        
        self.boton_probar = QPushButton("Probar URL")
        self.boton_probar.setMinimumWidth(100)
        layout_botones.addWidget(self.boton_probar)
        
        texto_aceptar = "Actualizar" if self._es_edicion else "Crear"
        self.boton_aceptar = QPushButton(texto_aceptar)
        self.boton_aceptar.setMinimumWidth(100)
        self.boton_aceptar.setDefault(True)
        layout_botones.addWidget(self.boton_aceptar)
        
        layout_padre.addLayout(layout_botones)
    
    def _configurar_validaciones(self) -> None:
        self.campo_titulo.textChanged.connect(self._validar_formulario)
        self.campo_url.textChanged.connect(self._validar_formulario)
        self.campo_categoria.currentTextChanged.connect(self._validar_formulario)
        self.campo_url.editingFinished.connect(self._limpiar_url)
    
    def _cargar_datos_existentes(self) -> None:
        if not self._es_edicion or not self._enlace_existente:
            return
        
        self.campo_titulo.setText(self._enlace_existente.get('titulo', ''))
        self.campo_url.setText(self._enlace_existente.get('url', ''))
        self.campo_categoria.setCurrentText(self._enlace_existente.get('categoria', ''))
        
        tags = self._enlace_existente.get('tags', [])
        if isinstance(tags, list):
            self.campo_tags.setPlainText(', '.join(tags))
    
    def _conectar_senales(self) -> None:
        self.boton_aceptar.clicked.connect(self._aceptar)
        self.boton_cancelar.clicked.connect(self.reject)
        self.boton_probar.clicked.connect(self._probar_url)
        self._validar_formulario()
    
    def _validar_formulario(self) -> None:
        titulo_valido = validar_titulo(self.campo_titulo.text())
        url_valida = validar_url(limpiar_url(self.campo_url.text()))
        categoria_valida = validar_categoria(self.campo_categoria.currentText())
        
        formulario_valido = titulo_valido and url_valida and categoria_valida
        self.boton_aceptar.setEnabled(formulario_valido)
        
        self._actualizar_estilo_campo(self.campo_titulo, titulo_valido)
        self._actualizar_estilo_campo(self.campo_url, url_valida)
        self._actualizar_estilo_campo(self.campo_categoria.lineEdit(), categoria_valida)
    
    def _actualizar_estilo_campo(self, campo, es_valido: bool) -> None:
        if hasattr(campo, 'text') and campo.text().strip():
            if es_valido:
                campo.setStyleSheet("")
            else:
                campo.setStyleSheet("border: 2px solid red;")
        else:
            campo.setStyleSheet("")
    
    def _limpiar_url(self) -> None:
        url_actual = self.campo_url.text()
        url_limpia = limpiar_url(url_actual)
        
        if url_limpia != url_actual:
            self.campo_url.setText(url_limpia)
    
    def _probar_url(self) -> None:
        url = limpiar_url(self.campo_url.text())
        
        if not validar_url(url):
            QMessageBox.warning(self, "URL Inválida", 
                              "La URL no es válida. Debe comenzar con http:// o https://")
            return
        
        from ..utils.io import abrir_url
        if abrir_url(url):
            QMessageBox.information(self, "URL Abierta", 
                                  f"URL abierta en el navegador: {url}")
        else:
            QMessageBox.warning(self, "Error", 
                              "No se pudo abrir la URL en el navegador.")
    
    def _aceptar(self) -> None:
        datos = self._obtener_datos_formulario()
        
        if not self._validar_datos_completos(datos):
            return
        
        self.enlace_aceptado.emit(datos)
        self.accept()
    
    def _obtener_datos_formulario(self) -> Dict[str, Any]:
        texto_tags = self.campo_tags.toPlainText().strip()
        tags = []
        if texto_tags:
            tags = [tag.strip() for tag in texto_tags.split(',') if tag.strip()]
        
        datos = {
            'titulo': self.campo_titulo.text().strip(),
            'url': limpiar_url(self.campo_url.text()),
            'categoria': self.campo_categoria.currentText().strip(),
            'tags': tags
        }
        
        if self._es_edicion and self._enlace_existente:
            datos['id'] = self._enlace_existente.get('id')
        
        return datos
    
    def _validar_datos_completos(self, datos: Dict[str, Any]) -> bool:
        errores = []
        
        if not validar_titulo(datos['titulo']):
            errores.append("El título es obligatorio")
        
        if not validar_url(datos['url']):
            errores.append("La URL debe ser válida y comenzar con http:// o https://")
        
        if not validar_categoria(datos['categoria']):
            errores.append("La categoría es obligatoria")
        
        if errores:
            texto_errores = "Por favor corrige los siguientes errores:\n\n"
            for error in errores:
                texto_errores += f"• {error}\n"
            
            QMessageBox.warning(self, "Datos Inválidos", texto_errores)
            return False
        
        return True
    
    def obtener_datos(self) -> Optional[Dict[str, Any]]:
        if self.result() == QDialog.DialogCode.Accepted:
            return self._obtener_datos_formulario()
        return None
    
    def es_edicion(self) -> bool:
        return self._es_edicion
    
    def obtener_id_enlace(self) -> Optional[str]:
        if self._es_edicion and self._enlace_existente:
            return self._enlace_existente.get('id')
        return None