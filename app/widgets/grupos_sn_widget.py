"""
Widget para gestión de Grupos de Service Now.
"""

import json
import logging
from typing import List, Dict, Any, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QListWidget, QListWidgetItem, QTextEdit, QPushButton,
    QSplitter, QFrame, QScrollArea, QSizePolicy, QDialog,
    QFormLayout, QDialogButtonBox, QMessageBox, QTextBrowser
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from app.theme.colors import Colors
from app.theme.fonts import Fonts

logger = logging.getLogger(__name__)


class GruposSNWidget(QWidget):
    """Widget para gestionar grupos de Service Now con búsqueda y filtrado."""
    
    grupo_seleccionado = pyqtSignal(dict)  # Señal cuando se selecciona un grupo
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grupos_data = []  # Lista de grupos de Service Now
        self.grupos_filtrados = []  # Lista filtrada actual
        self._setup_ui()
        self._cargar_datos_ejemplo()
        self._conectar_senales()
        
    def _setup_ui(self):
        """Configura la interfaz de usuario."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 10)  # Reducir márgenes
        layout.setSpacing(8)  # Reducir espaciado
        
        # Título más compacto
        titulo = QLabel("📋 Grupos de Service Now")
        titulo.setFont(Fonts.get_header_font())  # Usar header en lugar de title
        titulo.setStyleSheet(f"""
            color: {Colors.ACCENT_NEO};
            font-weight: bold;
            margin: 2px 0px;
            padding: 2px 0px;
        """)
        layout.addWidget(titulo)
        
    def _setup_ui(self):
        """Configura la interfaz de usuario."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 3, 8, 8)  # Márgenes más compactos
        layout.setSpacing(5)  # Espaciado más reducido
        
        # Título más compacto
        titulo = QLabel("📋 Grupos SN")  # Título más corto
        titulo.setFont(Fonts.get_monospace_font(Fonts.SIZE_MEDIUM, bold=True))  # Fuente más pequeña
        titulo.setStyleSheet(f"""
            color: {Colors.ACCENT_NEO};
            font-weight: bold;
            margin: 0px;
            padding: 1px 0px;
            max-height: 20px;
        """)
        titulo.setMaximumHeight(22)  # Altura máxima fija
        layout.addWidget(titulo)
        
        # Buscador más compacto
        search_layout = QHBoxLayout()
        search_layout.setSpacing(8)
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        search_label = QLabel("🔍")  # Solo icono
        search_label.setFont(Fonts.get_monospace_font(Fonts.SIZE_SMALL))
        search_label.setStyleSheet(f"color: {Colors.FG}; max-width: 20px;")
        search_label.setMaximumWidth(25)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar grupos...")  # Placeholder más corto
        self.search_input.setFont(Fonts.get_monospace_font(Fonts.SIZE_SMALL))
        self.search_input.setMaximumHeight(28)  # Altura fija más pequeña
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {Colors.BG2};
                border: 1px solid {Colors.BORDER};
                border-radius: 4px;
                padding: 4px 8px;
                color: {Colors.FG};
                max-height: 26px;
            }}
            QLineEdit:focus {{
                border-color: {Colors.ACCENT_NEO};
            }}
        """)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Splitter principal - más compacto
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background-color: {Colors.BORDER};
                width: 2px;
            }}
            QSplitter::handle:hover {{
                background-color: {Colors.ACCENT_NEO};
            }}
        """)
        splitter.setContentsMargins(0, 0, 0, 0)
        
        # Panel izquierdo - Lista de grupos (más compacto)
        left_panel = QFrame()
        left_panel.setFrameStyle(QFrame.Shape.StyledPanel)
        left_panel.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG1};
                border: 1px solid {Colors.BORDER};
                border-radius: 6px;
            }}
        """)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(6, 4, 6, 6)
        left_layout.setSpacing(4)
        
        grupos_label = QLabel("📁 Grupos:")  # Label más corto
        grupos_label.setFont(Fonts.get_monospace_font(Fonts.SIZE_SMALL, bold=True))
        grupos_label.setStyleSheet(f"color: {Colors.FG}; margin: 0px; max-height: 18px;")
        grupos_label.setMaximumHeight(20)
        left_layout.addWidget(grupos_label)
        
        self.grupos_list = QListWidget()
        self.grupos_list.setFont(Fonts.get_monospace_font(Fonts.SIZE_SMALL))
        self.grupos_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {Colors.BG2};
                border: 1px solid {Colors.BORDER};
                border-radius: 4px;
                padding: 2px;
                color: {Colors.FG};
            }}
            QListWidget::item {{
                padding: 6px;
                border-bottom: 1px solid {Colors.BORDER};
                border-radius: 3px;
                margin: 1px;
                max-height: 45px;
            }}
            QListWidget::item:hover {{
                background-color: {Colors.HOVER};
            }}
            QListWidget::item:selected {{
                background-color: {Colors.SELECTED};
                border: 1px solid {Colors.ACCENT_NEO};
            }}
        """)
        left_layout.addWidget(self.grupos_list)
        
        # Botones de acción más compactos
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(4)
        botones_layout.setContentsMargins(0, 4, 0, 0)
        
        self.btn_nuevo = QPushButton("➕")
        self.btn_nuevo.setToolTip("Crear nuevo grupo")
        self.btn_editar = QPushButton("✏️")
        self.btn_editar.setToolTip("Editar grupo seleccionado")
        self.btn_eliminar = QPushButton("🗑️")
        self.btn_eliminar.setToolTip("Eliminar grupo seleccionado")
        
        for btn in [self.btn_nuevo, self.btn_editar, self.btn_eliminar]:
            btn.setFont(Fonts.get_monospace_font(Fonts.SIZE_SMALL))
            btn.setMaximumHeight(28)
            btn.setMaximumWidth(35)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Colors.BG2};
                    border: 1px solid {Colors.BORDER};
                    border-radius: 4px;
                    padding: 4px;
                    color: {Colors.FG};
                    font-weight: bold;
                    max-width: 32px;
                    max-height: 26px;
                }}
                QPushButton:hover {{
                    background-color: {Colors.HOVER};
                    border-color: {Colors.ACCENT_NEO};
                }}
                QPushButton:pressed {{
                    background-color: {Colors.PRESSED};
                }}
                QPushButton:disabled {{
                    opacity: 0.5;
                }}
            """)
            botones_layout.addWidget(btn)
        
        # Agregar espacio flexible para centrar botones
        botones_layout.addStretch()
        
        # Inicialmente deshabilitar botones que requieren selección
        self.btn_editar.setEnabled(False)
        self.btn_eliminar.setEnabled(False)
        
        left_layout.addLayout(botones_layout)
        
        # Panel derecho - Detalles del grupo (más compacto)
        right_panel = QFrame()
        right_panel.setFrameStyle(QFrame.Shape.StyledPanel)
        right_panel.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG1};
                border: 1px solid {Colors.BORDER};
                border-radius: 6px;
            }}
        """)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(6, 4, 6, 6)
        right_layout.setSpacing(4)
        
        detalles_label = QLabel("📄 Detalles:")  # Label más corto
        detalles_label.setFont(Fonts.get_monospace_font(Fonts.SIZE_SMALL, bold=True))
        detalles_label.setStyleSheet(f"color: {Colors.FG}; margin: 0px; max-height: 18px;")
        detalles_label.setMaximumHeight(20)
        right_layout.addWidget(detalles_label)
        
        self.detalles_text = QTextEdit()
        self.detalles_text.setReadOnly(True)
        self.detalles_text.setFont(Fonts.get_monospace_font(Fonts.SIZE_SMALL))
        self.detalles_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Colors.BG2};
                border: 1px solid {Colors.BORDER};
                border-radius: 4px;
                padding: 8px;
                color: {Colors.FG};
            }}
        """)
        self.detalles_text.setHtml("""
            <div style="text-align: center; margin-top: 30px;">
                <h4 style="color: #666;">Selecciona un grupo para ver detalles</h4>
            </div>
        """)
        right_layout.addWidget(self.detalles_text)
        
        # Configurar splitter con proporciones optimizadas
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([280, 450])  # Proporción más equilibrada
        
        layout.addWidget(splitter)
        
    def _conectar_senales(self):
        """Conecta las señales de la interfaz."""
        self.search_input.textChanged.connect(self._filtrar_grupos)
        self.grupos_list.itemSelectionChanged.connect(self._on_grupo_seleccionado)
        self.btn_nuevo.clicked.connect(self._crear_grupo)
        self.btn_editar.clicked.connect(self._editar_grupo)
        self.btn_eliminar.clicked.connect(self._eliminar_grupo)
        
    def _cargar_datos_ejemplo(self):
        """Carga datos de ejemplo de grupos de Service Now."""
        self.grupos_data = [
            {
                "id": "grp_001",
                "nombre": "Incident Management",
                "descripcion": "Grupo encargado de la gestión de incidentes en Service Now",
                "responsabilidades": [
                    "Clasificación y priorización de incidentes",
                    "Resolución de incidentes de nivel 1",
                    "Escalamiento a grupos especializados",
                    "Comunicación con usuarios afectados"
                ],
                "miembros": ["admin.user", "incident.manager", "tech.support"],
                "manager": "incident.manager",
                "email": "incident-team@company.com",
                "sla": "4 horas para P1, 8 horas para P2",
                "horario": "24/7",
                "tools": ["Service Now", "Teams", "Email"],
                "estado": "Activo"
            },
            {
                "id": "grp_002",
                "nombre": "Change Management",
                "descripcion": "Gestión y aprobación de cambios en la infraestructura",
                "responsabilidades": [
                    "Evaluación de riesgos de cambios",
                    "Aprobación de cambios críticos",
                    "Coordinación de ventanas de mantenimiento",
                    "Documentación post-implementación"
                ],
                "miembros": ["change.manager", "arch.lead", "ops.manager"],
                "manager": "change.manager",
                "email": "change-management@company.com",
                "sla": "2 días hábiles para evaluación",
                "horario": "Lunes a Viernes 9-17",
                "tools": ["Service Now", "SharePoint", "Visio"],
                "estado": "Activo"
            },
            {
                "id": "grp_003",
                "nombre": "Network Operations",
                "descripcion": "Monitoreo y mantenimiento de infraestructura de red",
                "responsabilidades": [
                    "Monitoreo 24/7 de equipos de red",
                    "Resolución de problemas de conectividad",
                    "Mantenimiento preventivo",
                    "Gestión de configuraciones de red"
                ],
                "miembros": ["network.admin", "noc.engineer", "net.specialist"],
                "manager": "network.admin",
                "email": "network-ops@company.com",
                "sla": "15 minutos para P1, 1 hora para P2",
                "horario": "24/7",
                "tools": ["PRTG", "SolarWinds", "Service Now"],
                "estado": "Activo"
            },
            {
                "id": "grp_004",
                "nombre": "Database Administration",
                "descripcion": "Administración y mantenimiento de bases de datos",
                "responsabilidades": [
                    "Backup y recovery de bases de datos",
                    "Optimización de rendimiento",
                    "Gestión de accesos y seguridad",
                    "Monitoreo de espacio y recursos"
                ],
                "miembros": ["dba.senior", "db.analyst", "backup.admin"],
                "manager": "dba.senior",
                "email": "dba-team@company.com",
                "sla": "1 hora para P1, 4 horas para P2",
                "horario": "24/7 on-call",
                "tools": ["SQL Server", "Oracle", "MySQL", "Service Now"],
                "estado": "Activo"
            },
            {
                "id": "grp_005",
                "nombre": "Security Operations",
                "descripcion": "Monitoreo y respuesta a incidentes de seguridad",
                "responsabilidades": [
                    "Monitoreo de eventos de seguridad",
                    "Investigación de incidentes",
                    "Implementación de políticas de seguridad",
                    "Gestión de vulnerabilidades"
                ],
                "miembros": ["sec.analyst", "soc.manager", "forensic.expert"],
                "manager": "soc.manager",
                "email": "security-ops@company.com",
                "sla": "Inmediato para P1, 30 min para P2",
                "horario": "24/7",
                "tools": ["SIEM", "Splunk", "Nessus", "Service Now"],
                "estado": "Activo"
            }
        ]
        
        self.grupos_filtrados = self.grupos_data.copy()
        self._actualizar_lista_grupos()
        
    def _filtrar_grupos(self):
        """Filtra los grupos basado en el texto de búsqueda."""
        texto_busqueda = self.search_input.text().lower().strip()
        
        if not texto_busqueda:
            self.grupos_filtrados = self.grupos_data.copy()
        else:
            self.grupos_filtrados = []
            for grupo in self.grupos_data:
                # Buscar en nombre, descripción y responsabilidades
                if (texto_busqueda in grupo['nombre'].lower() or
                    texto_busqueda in grupo['descripcion'].lower() or
                    any(texto_busqueda in resp.lower() for resp in grupo['responsabilidades'])):
                    self.grupos_filtrados.append(grupo)
        
        self._actualizar_lista_grupos()
        
    def _actualizar_lista_grupos(self):
        """Actualiza la lista visual de grupos."""
        self.grupos_list.clear()
        
        for grupo in self.grupos_filtrados:
            # Texto más compacto para la lista
            item_text = f"📋 {grupo['nombre']}\n   {grupo['descripcion'][:35]}..."
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, grupo)  # Almacenar datos del grupo
            self.grupos_list.addItem(item)
            
    def _on_grupo_seleccionado(self):
        """Maneja la selección de un grupo en la lista."""
        item_actual = self.grupos_list.currentItem()
        
        if item_actual:
            grupo = item_actual.data(Qt.ItemDataRole.UserRole)
            self._mostrar_detalles_grupo(grupo)
            self.btn_editar.setEnabled(True)
            self.btn_eliminar.setEnabled(True)
            self.grupo_seleccionado.emit(grupo)
        else:
            self._limpiar_detalles()
            self.btn_editar.setEnabled(False)
            self.btn_eliminar.setEnabled(False)
            
    def _mostrar_detalles_grupo(self, grupo: Dict[str, Any]):
        """Muestra los detalles del grupo seleccionado."""
        responsabilidades_html = "".join([f"<li style='margin: 2px 0;'>{resp}</li>" for resp in grupo['responsabilidades']])
        miembros_html = "".join([f"<li style='margin: 1px 0;'>{miembro}</li>" for miembro in grupo['miembros']])
        tools_html = "".join([f"<li style='margin: 1px 0;'>{tool}</li>" for tool in grupo['tools']])
        
        html_content = f"""
        <div style="color: {Colors.FG}; font-size: 11px; line-height: 1.3;">
            <h3 style="color: {Colors.ACCENT_NEO}; margin: 0 0 8px 0; font-size: 14px;">
                📋 {grupo['nombre']}
            </h3>
            
            <div style="margin-bottom: 8px;">
                <h4 style="color: {Colors.ACCENT_CYAN}; margin: 0 0 3px 0; font-size: 12px;">📝 Descripción:</h4>
                <p style="margin: 0 0 0 15px; font-size: 11px;">{grupo['descripcion']}</p>
            </div>
            
            <div style="margin-bottom: 8px;">
                <h4 style="color: {Colors.ACCENT_CYAN}; margin: 0 0 3px 0; font-size: 12px;">🎯 Responsabilidades:</h4>
                <ul style="margin: 0 0 0 15px; padding-left: 15px; font-size: 10px;">
                    {responsabilidades_html}
                </ul>
            </div>
            
            <div style="margin-bottom: 8px;">
                <h4 style="color: {Colors.ACCENT_CYAN}; margin: 0 0 3px 0; font-size: 12px;">👥 Miembros:</h4>
                <ul style="margin: 0 0 0 15px; padding-left: 15px; font-size: 10px;">
                    {miembros_html}
                </ul>
            </div>
            
            <div style="margin-bottom: 6px;">
                <h4 style="color: {Colors.ACCENT_CYAN}; margin: 0 0 2px 0; font-size: 12px;">👨‍💼 Manager:</h4>
                <p style="margin: 0 0 0 15px; font-size: 11px;">{grupo['manager']}</p>
            </div>
            
            <div style="margin-bottom: 6px;">
                <h4 style="color: {Colors.ACCENT_CYAN}; margin: 0 0 2px 0; font-size: 12px;">📧 Email:</h4>
                <p style="margin: 0 0 0 15px; font-size: 11px;">{grupo['email']}</p>
            </div>
            
            <div style="margin-bottom: 6px;">
                <h4 style="color: {Colors.ACCENT_CYAN}; margin: 0 0 2px 0; font-size: 12px;">⏱️ SLA:</h4>
                <p style="margin: 0 0 0 15px; font-size: 11px;">{grupo['sla']}</p>
            </div>
            
            <div style="margin-bottom: 6px;">
                <h4 style="color: {Colors.ACCENT_CYAN}; margin: 0 0 2px 0; font-size: 12px;">🕐 Horario:</h4>
                <p style="margin: 0 0 0 15px; font-size: 11px;">{grupo['horario']}</p>
            </div>
            
            <div style="margin-bottom: 6px;">
                <h4 style="color: {Colors.ACCENT_CYAN}; margin: 0 0 3px 0; font-size: 12px;">🛠️ Herramientas:</h4>
                <ul style="margin: 0 0 0 15px; padding-left: 15px; font-size: 10px;">
                    {tools_html}
                </ul>
            </div>
            
            <div style="margin-bottom: 4px;">
                <h4 style="color: {Colors.ACCENT_CYAN}; margin: 0 0 2px 0; font-size: 12px;">📊 Estado:</h4>
                <p style="margin: 0 0 0 15px; color: {Colors.ACCENT_NEO}; font-size: 11px;">
                    <strong>{grupo['estado']}</strong>
                </p>
            </div>
        </div>
        """
        
        self.detalles_text.setHtml(html_content)
        
    def _limpiar_detalles(self):
        """Limpia el panel de detalles."""
        self.detalles_text.setHtml("""
            <div style="text-align: center; margin-top: 50px;">
                <h3 style="color: #666;">Selecciona un grupo para ver sus detalles</h3>
            </div>
        """)
        
    def _crear_grupo(self):
        """Crea un nuevo grupo."""
        dialog = GrupoDialog(self)
        dialog.setWindowTitle("Crear Nuevo Grupo")
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            nuevo_grupo = dialog.obtener_datos()
            nuevo_grupo["id"] = f"grp_{len(self.grupos_data) + 1:03d}"
            
            self.grupos_data.append(nuevo_grupo)
            self._filtrar_grupos()  # Actualizar la vista
            
            # Mostrar mensaje de confirmación
            QMessageBox.information(
                self, 
                "Grupo Creado", 
                f"El grupo '{nuevo_grupo['nombre']}' ha sido creado exitosamente."
            )
            logger.info(f"Nuevo grupo creado: {nuevo_grupo['nombre']}")
        
    def _editar_grupo(self):
        """Edita el grupo seleccionado."""
        item_actual = self.grupos_list.currentItem()
        if not item_actual:
            return
            
        grupo = item_actual.data(Qt.ItemDataRole.UserRole)
        dialog = GrupoDialog(self, grupo)
        dialog.setWindowTitle(f"Editar Grupo: {grupo['nombre']}")
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            datos_actualizados = dialog.obtener_datos()
            
            # Actualizar el grupo en la lista
            for i, g in enumerate(self.grupos_data):
                if g["id"] == grupo["id"]:
                    # Mantener el ID original
                    datos_actualizados["id"] = grupo["id"]
                    self.grupos_data[i] = datos_actualizados
                    break
            
            self._filtrar_grupos()  # Actualizar la vista
            self._mostrar_detalles_grupo(datos_actualizados)  # Actualizar detalles
            
            QMessageBox.information(
                self, 
                "Grupo Actualizado", 
                f"El grupo '{datos_actualizados['nombre']}' ha sido actualizado exitosamente."
            )
            logger.info(f"Grupo editado: {datos_actualizados['nombre']}")
            
    def _eliminar_grupo(self):
        """Elimina el grupo seleccionado."""
        item_actual = self.grupos_list.currentItem()
        if not item_actual:
            return
            
        grupo = item_actual.data(Qt.ItemDataRole.UserRole)
        
        # Confirmar eliminación
        respuesta = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Estás seguro de que deseas eliminar el grupo '{grupo['nombre']}'?\n\n"
            "Esta acción no se puede deshacer.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            # Eliminar de la lista
            self.grupos_data = [g for g in self.grupos_data if g["id"] != grupo["id"]]
            
            self._filtrar_grupos()  # Actualizar la vista
            self._limpiar_detalles()  # Limpiar panel de detalles
            
            QMessageBox.information(
                self, 
                "Grupo Eliminado", 
                f"El grupo '{grupo['nombre']}' ha sido eliminado exitosamente."
            )
            logger.info(f"Grupo eliminado: {grupo['nombre']}")


class GrupoDialog(QDialog):
    """Diálogo para crear/editar grupos de Service Now."""
    
    def __init__(self, parent=None, grupo_data=None):
        super().__init__(parent)
        self.grupo_data = grupo_data
        self.setModal(True)
        self.setMinimumSize(500, 600)
        self._setup_ui()
        
        if grupo_data:
            self._cargar_datos(grupo_data)
    
    def _setup_ui(self):
        """Configura la interfaz del diálogo."""
        layout = QVBoxLayout(self)
        
        # Formulario
        form_layout = QFormLayout()
        
        # Campos del formulario
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Ej: Incident Management")
        
        self.descripcion_input = QLineEdit()
        self.descripcion_input.setPlaceholderText("Descripción breve del grupo")
        
        self.responsabilidades_input = QTextEdit()
        self.responsabilidades_input.setPlaceholderText("Una responsabilidad por línea")
        self.responsabilidades_input.setMaximumHeight(100)
        
        self.miembros_input = QLineEdit()
        self.miembros_input.setPlaceholderText("Separar con comas: user1, user2, user3")
        
        self.manager_input = QLineEdit()
        self.manager_input.setPlaceholderText("usuario.manager")
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("grupo@company.com")
        
        self.sla_input = QLineEdit()
        self.sla_input.setPlaceholderText("Ej: 4 horas para P1, 8 horas para P2")
        
        self.horario_input = QLineEdit()
        self.horario_input.setPlaceholderText("Ej: 24/7 o Lunes a Viernes 9-17")
        
        self.tools_input = QLineEdit()
        self.tools_input.setPlaceholderText("Separar con comas: Tool1, Tool2, Tool3")
        
        self.estado_input = QLineEdit()
        self.estado_input.setText("Activo")
        
        # Agregar campos al formulario
        form_layout.addRow("Nombre:", self.nombre_input)
        form_layout.addRow("Descripción:", self.descripcion_input)
        form_layout.addRow("Responsabilidades:", self.responsabilidades_input)
        form_layout.addRow("Miembros:", self.miembros_input)
        form_layout.addRow("Manager:", self.manager_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("SLA:", self.sla_input)
        form_layout.addRow("Horario:", self.horario_input)
        form_layout.addRow("Herramientas:", self.tools_input)
        form_layout.addRow("Estado:", self.estado_input)
        
        layout.addLayout(form_layout)
        
        # Botones
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._validar_y_aceptar)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        
        # Aplicar estilos
        self._aplicar_estilos()
    
    def _aplicar_estilos(self):
        """Aplica estilos al diálogo."""
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {Colors.BG1};
                color: {Colors.FG};
            }}
            QLabel {{
                color: {Colors.FG};
                font-weight: bold;
            }}
            QLineEdit, QTextEdit {{
                background-color: {Colors.BG2};
                border: 1px solid {Colors.BORDER};
                border-radius: 4px;
                padding: 6px;
                color: {Colors.FG};
            }}
            QLineEdit:focus, QTextEdit:focus {{
                border-color: {Colors.ACCENT_NEO};
            }}
            QPushButton {{
                background-color: {Colors.BG2};
                border: 1px solid {Colors.BORDER};
                border-radius: 4px;
                padding: 8px 16px;
                color: {Colors.FG};
            }}
            QPushButton:hover {{
                background-color: {Colors.HOVER};
                border-color: {Colors.ACCENT_NEO};
            }}
        """)
    
    def _cargar_datos(self, grupo_data):
        """Carga los datos del grupo en el formulario."""
        self.nombre_input.setText(grupo_data.get('nombre', ''))
        self.descripcion_input.setText(grupo_data.get('descripcion', ''))
        self.responsabilidades_input.setText('\n'.join(grupo_data.get('responsabilidades', [])))
        self.miembros_input.setText(', '.join(grupo_data.get('miembros', [])))
        self.manager_input.setText(grupo_data.get('manager', ''))
        self.email_input.setText(grupo_data.get('email', ''))
        self.sla_input.setText(grupo_data.get('sla', ''))
        self.horario_input.setText(grupo_data.get('horario', ''))
        self.tools_input.setText(', '.join(grupo_data.get('tools', [])))
        self.estado_input.setText(grupo_data.get('estado', 'Activo'))
    
    def _validar_y_aceptar(self):
        """Valida los datos antes de aceptar."""
        if not self.nombre_input.text().strip():
            QMessageBox.warning(self, "Error", "El nombre del grupo es obligatorio.")
            return
        
        if not self.descripcion_input.text().strip():
            QMessageBox.warning(self, "Error", "La descripción del grupo es obligatoria.")
            return
            
        self.accept()
    
    def obtener_datos(self):
        """Obtiene los datos del formulario."""
        responsabilidades = [
            resp.strip() for resp in self.responsabilidades_input.toPlainText().split('\n')
            if resp.strip()
        ]
        
        miembros = [
            miembro.strip() for miembro in self.miembros_input.text().split(',')
            if miembro.strip()
        ]
        
        tools = [
            tool.strip() for tool in self.tools_input.text().split(',')
            if tool.strip()
        ]
        
        return {
            "nombre": self.nombre_input.text().strip(),
            "descripcion": self.descripcion_input.text().strip(),
            "responsabilidades": responsabilidades,
            "miembros": miembros,
            "manager": self.manager_input.text().strip(),
            "email": self.email_input.text().strip(),
            "sla": self.sla_input.text().strip(),
            "horario": self.horario_input.text().strip(),
            "tools": tools,
            "estado": self.estado_input.text().strip()
        }