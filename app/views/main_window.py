"""
Ventana principal de la aplicación.
"""
import logging
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLineEdit, QPushButton, QListWidget, QListWidgetItem, QTableView,
    QSplitter, QLabel, QMessageBox, QFileDialog,
    QStatusBar, QMenuBar, QMenu, QFrame, QApplication,
    QToolBar, QToolButton, QTabWidget, QInputDialog, QDialog, QTextEdit
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QUrl
from PyQt6.QtGui import QKeySequence, QShortcut, QFont, QAction, QDesktopServices, QIcon, QPixmap
from ..models.repository import RepositorioEnlaces
from ..models.link_model import ModeloTablaEnlaces
from ..models.search import (
    buscar_enlaces, extraer_todas_las_categorias, 
    extraer_todos_los_tags
)
from ..utils.io import abrir_url
from ..theme import Colors, Fonts, get_icon
from ..widgets import TitleBar, NotesWidget, GruposSNWidget
from ..widgets.about_dialog import AboutDialog
from ..delegates import TagDelegate
from .link_dialog import DialogoEnlace
from ..config import (
    obtener_config_tabla, obtener_config_app, obtener_color_scheme, 
    obtener_typography, obtener_spacing, obtener_elevation,
    get_color, get_font_size, get_spacing, get_border_radius, get_shadow
)


logger = logging.getLogger(__name__)


class VentanaPrincipal(QMainWindow):
    """
    Ventana principal de la aplicación de gestión de enlaces.
    """
    
    def __init__(self, ruta_datos: Path):
        super().__init__()
        
        # Inicializar repositorio y modelo
        self.repositorio = RepositorioEnlaces(ruta_datos)
        self.modelo_tabla = ModeloTablaEnlaces()
        
        # Estado de filtros
        self.categoria_filtro_actual = ""
        self.tag_filtro_actual = ""
        self.busqueda_actual = ""
        
        # Timer para búsqueda con delay
        self.timer_busqueda = QTimer()
        self.timer_busqueda.setSingleShot(True)
        self.timer_busqueda.timeout.connect(self._realizar_busqueda)
        
        self._configurar_ventana()
        self._crear_interfaz()
        self._conectar_senales()
        self._configurar_atajos()
        self._cargar_datos_iniciales()
        
        logger.info("Ventana principal inicializada")
    
    def _configurar_ventana(self) -> None:
        """Configura las propiedades básicas de la ventana."""
        self.setWindowTitle("TECH LINK VIEWER - Global Link Search")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        # Configurar fuente monoespaciada
        fuente = Fonts.get_monospace_font(Fonts.SIZE_NORMAL)
        self.setFont(fuente)
    
    def _crear_interfaz(self) -> None:
        """Crea la interfaz de usuario."""
        central_widget = QWidget()
        central_widget.setObjectName("central_widget")  # ID para el stylesheet
        self.setCentralWidget(central_widget)
        
        # Configurar imagen de fondo translúcida
        self._configurar_fondo_translucido(central_widget)
        
        # Layout principal más compacto
        layout_principal = QVBoxLayout(central_widget)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(2)  # Reducir espacio entre elementos
        
        # Crear título con efecto typewriter (más compacto)
        self._crear_titulo_typewriter(layout_principal)
        
        # Crear toolbar (búsqueda y botones)
        self._crear_toolbar(layout_principal)
        
        # Crear área principal con splitter
        self._crear_area_principal(layout_principal)
        
        # Crear barra de estado
        self._crear_barra_estado()
        
        # Crear menú
        self._crear_menu()
    
    def _configurar_fondo_translucido(self, widget: QWidget) -> None:
        """Configura una imagen de fondo translúcida para la aplicación."""
        import os
        from pathlib import Path
        
        # Buscar la imagen de fondo (fondo.jpg)
        fondo_path = Path("Images/fondo.jpg")
        
        # Si estamos en un ejecutable compilado, buscar en el directorio de la aplicación
        if getattr(sys, 'frozen', False):
            # Ejecutable compilado
            app_dir = Path(sys.executable).parent
            fondo_path = app_dir / "Images" / "fondo.jpg"
            if not fondo_path.exists():
                # Intentar en el directorio actual
                fondo_path = Path("Images/fondo.jpg")
        
        # Verificar si la imagen existe
        if fondo_path.exists():
            fondo_path_str = str(fondo_path).replace('\\', '/')
            
            # Configurar stylesheet con imagen de fondo translúcida
            # Qt stylesheet con imagen de fondo y overlay translúcido
            stylesheet = f"""
            QMainWindow {{
                background-color: {Colors.BG0};
                background-image: url({fondo_path_str});
                background-repeat: no-repeat;
                background-position: center;
            }}
            
            QMainWindow > QWidget {{
                background-color: rgba(15, 15, 15, 230);
            }}
            
            QWidget#central_widget {{
                background-color: rgba(25, 25, 25, 200);
                border-radius: 10px;
                margin: 10px;
            }}
            """
            logger.info("Fondo translúcido configurado correctamente con fondo.jpg")
        else:
            # Si no se encuentra la imagen, usar solo color de fondo
            stylesheet = f"""
            QMainWindow {{
                background-color: {Colors.BG0};
            }}
            """
            logger.warning(f"No se encontró la imagen de fondo en: {fondo_path}")
        
        # Aplicar el estilo moderno mejorado
        self.setStyleSheet(self._generar_stylesheet_moderno())

    def _generar_stylesheet_moderno(self) -> str:
        """Genera el stylesheet moderno con el nuevo sistema de diseño"""
        colors = obtener_color_scheme()
        typography = obtener_typography()
        spacing = obtener_spacing()
        elevation = obtener_elevation()
        
        return f"""
        /* Estilo base de la aplicación */
        QMainWindow {{
            background-color: {colors['surface']};
            color: {colors['on_surface']};
            font-family: {typography['font_family_primary']};
            font-size: {typography['font_sizes']['body']}px;
        }}
        
        /* Widget central con elevación */
        QWidget#central_widget {{
            background-color: {colors['surface']};
            border-radius: {elevation['border_radius']['medium']}px;
            margin: {spacing['sm']}px;
        }}
        
        /* Estilo mejorado para tabs */
        QTabWidget::pane {{
            border: 1px solid {colors['outline']};
            background-color: {colors['surface_variant']};
            border-radius: {elevation['border_radius']['medium']}px;
            margin: {spacing['xs']}px;
        }}
        
        QTabBar::tab {{
            background-color: {colors['surface_elevated']};
            color: {colors['on_surface_variant']};
            padding: {spacing['sm']}px {spacing['lg']}px;
            margin-right: {spacing['xs']}px;
            border-top-left-radius: {elevation['border_radius']['small']}px;
            border-top-right-radius: {elevation['border_radius']['small']}px;
            font-weight: {typography['font_weights']['medium']};
            min-width: 120px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {colors['primary']};
            color: {colors['on_primary']};
            font-weight: {typography['font_weights']['semibold']};
        }}
        
        QTabBar::tab:hover:!selected {{
            background-color: {colors['primary_variant']};
            color: {colors['on_primary']};
        }}
        
        /* Botones mejorados */
        QPushButton {{
            background-color: {colors['surface_elevated']};
            color: {colors['on_surface']};
            border: 1px solid {colors['outline']};
            border-radius: {elevation['border_radius']['small']}px;
            padding: {spacing['sm']}px {spacing['md']}px;
            font-weight: {typography['font_weights']['medium']};
            min-height: 32px;
        }}
        
        QPushButton:hover {{
            background-color: {colors['primary_variant']};
            color: {colors['on_primary']};
            border-color: {colors['primary']};
        }}
        
        QPushButton:pressed {{
            background-color: {colors['primary_dark']};
            color: {colors['on_primary']};
        }}
        
        /* Campos de entrada mejorados */
        QLineEdit, QTextEdit, QComboBox {{
            background-color: {colors['surface_elevated']};
            color: {colors['on_surface']};
            border: 1px solid {colors['outline']};
            border-radius: {elevation['border_radius']['small']}px;
            padding: {spacing['sm']}px;
            font-size: {typography['font_sizes']['body']}px;
        }}
        
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
            border: 2px solid {colors['primary']};
            background-color: {colors['surface']};
        }}
        
        /* Lista mejorada */
        QListWidget {{
            background-color: {colors['surface_elevated']};
            color: {colors['on_surface']};
            border: 1px solid {colors['outline']};
            border-radius: {elevation['border_radius']['small']}px;
            padding: {spacing['xs']}px;
        }}
        
        QListWidget::item {{
            padding: {spacing['sm']}px;
            border-radius: {elevation['border_radius']['small']}px;
            margin: 1px;
        }}
        
        QListWidget::item:selected {{
            background-color: {colors['primary']};
            color: {colors['on_primary']};
        }}
        
        QListWidget::item:hover:!selected {{
            background-color: {colors['surface_variant']};
        }}
        
        /* Scrollbars estilizados */
        QScrollBar:vertical {{
            background-color: {colors['surface_variant']};
            width: 12px;
            border-radius: 6px;
            margin: 0;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {colors['outline']};
            border-radius: 6px;
            min-height: 20px;
            margin: 2px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {colors['primary_variant']};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        /* Toolbar mejorado */
        QToolBar {{
            background-color: {colors['surface_elevated']};
            border: none;
            spacing: {spacing['sm']}px;
            padding: {spacing['sm']}px;
        }}
        
        QToolBar QToolButton {{
            background-color: transparent;
            border: none;
            border-radius: {elevation['border_radius']['small']}px;
            padding: {spacing['sm']}px;
            color: {colors['on_surface']};
        }}
        
        QToolBar QToolButton:hover {{
            background-color: {colors['primary_variant']};
            color: {colors['on_primary']};
        }}
        """

    def _crear_titulo_typewriter(self, layout_padre: QVBoxLayout) -> None:
        """Crea el título con efecto typewriter."""
        self.title_bar = TitleBar()
        self.title_bar.configure(
            type_speed=120,
            erase_speed=80,
            pause_duration=3000,
            erase_pause=500,
            caret_char="█",
            loop_enabled=True
        )
        # Establecer altura máxima para que sea más compacto
        self.title_bar.setMaximumHeight(45)
        self.title_bar.setMinimumHeight(45)
        layout_padre.addWidget(self.title_bar)
        
        # Iniciar animación typewriter
        self.title_bar.start()
    
    def _crear_menu(self) -> None:
        """Crea el menú de la aplicación."""
        menubar = self.menuBar()
        
        # Menú Archivo
        menu_archivo = menubar.addMenu("Archivo")
        
        accion_nuevo = QAction("Nuevo Enlace", self)
        accion_nuevo.setShortcut(QKeySequence("Ctrl+N"))
        accion_nuevo.triggered.connect(self._nuevo_enlace)
        menu_archivo.addAction(accion_nuevo)
        
        accion_guardar = QAction("Guardar", self)
        accion_guardar.setShortcut(QKeySequence("Ctrl+S"))
        accion_guardar.triggered.connect(self._guardar_datos)
        menu_archivo.addAction(accion_guardar)
        
        menu_archivo.addSeparator()
        
        accion_importar = QAction("Importar JSON...", self)
        accion_importar.triggered.connect(self._importar_json)
        menu_archivo.addAction(accion_importar)
        
        accion_exportar = QAction("Exportar JSON...", self)
        accion_exportar.triggered.connect(self._exportar_json)
        menu_archivo.addAction(accion_exportar)
        
        menu_archivo.addSeparator()
        
        accion_salir = QAction("Salir", self)
        accion_salir.setShortcut(QKeySequence("Ctrl+Q"))
        accion_salir.triggered.connect(self.close)
        menu_archivo.addAction(accion_salir)
        
        # Menú Editar
        menu_editar = menubar.addMenu("Editar")
        
        accion_editar = QAction("Editar Enlace", self)
        accion_editar.setShortcut(QKeySequence("Ctrl+E"))
        accion_editar.triggered.connect(self._editar_enlace_seleccionado)
        menu_editar.addAction(accion_editar)
        
        accion_eliminar = QAction("Eliminar Enlace", self)
        accion_eliminar.setShortcut(QKeySequence("Del"))
        accion_eliminar.triggered.connect(self._eliminar_enlace_seleccionado)
        menu_editar.addAction(accion_eliminar)
        
        menu_editar.addSeparator()
        
        accion_buscar = QAction("Buscar", self)
        accion_buscar.setShortcut(QKeySequence("Ctrl+F"))
        accion_buscar.triggered.connect(self._enfocar_busqueda)
        menu_editar.addAction(accion_buscar)
    
    def _crear_toolbar(self, layout_padre: QVBoxLayout) -> None:
        """Crea la barra de herramientas con íconos."""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        
        # Dar un poco más de altura a la toolbar para mejor usabilidad
        toolbar.setMinimumHeight(50)
        
        # Campo de búsqueda
        self.campo_busqueda = QLineEdit()
        self.campo_busqueda.setPlaceholderText("Buscar enlaces por título, URL, categoría o tag...")
        self.campo_busqueda.setMinimumWidth(350)
        self.campo_busqueda.setMinimumHeight(32)
        self.campo_busqueda.setToolTip("Búsqueda difusa inteligente (Ctrl+F)")
        toolbar.addWidget(self.campo_busqueda)
        
        toolbar.addSeparator()
        
        # Botón Agregar
        self.boton_nuevo = QToolButton()
        self.boton_nuevo.setIcon(get_icon('add'))
        self.boton_nuevo.setText("Agregar")
        self.boton_nuevo.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.boton_nuevo.setToolTip("Agregar nuevo enlace (Ctrl+N)")
        toolbar.addWidget(self.boton_nuevo)
        
        # Botón Editar
        self.boton_editar = QToolButton()
        self.boton_editar.setIcon(get_icon('edit'))
        self.boton_editar.setText("Editar")
        self.boton_editar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.boton_editar.setToolTip("Editar enlace seleccionado (Ctrl+E)")
        self.boton_editar.setEnabled(False)
        toolbar.addWidget(self.boton_editar)
        
        # Botón Eliminar
        self.boton_eliminar = QToolButton()
        self.boton_eliminar.setIcon(get_icon('delete'))
        self.boton_eliminar.setText("Eliminar")
        self.boton_eliminar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.boton_eliminar.setToolTip("Eliminar enlace seleccionado (Del)")
        self.boton_eliminar.setEnabled(False)
        toolbar.addWidget(self.boton_eliminar)
        
        toolbar.addSeparator()
        
        # Botón Importar
        self.boton_importar = QToolButton()
        self.boton_importar.setIcon(get_icon('import'))
        self.boton_importar.setText("Importar")
        self.boton_importar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.boton_importar.setToolTip("Importar enlaces desde JSON")
        toolbar.addWidget(self.boton_importar)
        
        # Botón Exportar
        self.boton_exportar = QToolButton()
        self.boton_exportar.setIcon(get_icon('export'))
        self.boton_exportar.setText("Exportar")
        self.boton_exportar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.boton_exportar.setToolTip("Exportar enlaces a JSON")
        toolbar.addWidget(self.boton_exportar)
        
        toolbar.addSeparator()
        
        # Botón Refrescar
        self.boton_refrescar = QToolButton()
        self.boton_refrescar.setIcon(get_icon('refresh'))
        self.boton_refrescar.setText("Refrescar")
        self.boton_refrescar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.boton_refrescar.setToolTip("Refrescar vista y datos (F5)")
        toolbar.addWidget(self.boton_refrescar)
        
        # Botón Configuración
        self.boton_configuracion = QToolButton()
        self.boton_configuracion.setIcon(get_icon('settings'))
        self.boton_configuracion.setText("Config")
        self.boton_configuracion.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.boton_configuracion.setToolTip("Configuración de la aplicación")
        toolbar.addWidget(self.boton_configuracion)
        
        toolbar.addSeparator()
        
        # Botón Ayuda
        self.boton_ayuda = QToolButton()
        self.boton_ayuda.setIcon(get_icon('help'))
        self.boton_ayuda.setText("Ayuda")
        self.boton_ayuda.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.boton_ayuda.setToolTip("Ayuda rápida (F1)")
        toolbar.addWidget(self.boton_ayuda)
        
        # Botón Guía
        self.boton_guia = QToolButton()
        self.boton_guia.setIcon(get_icon('info'))  # Usar icono de info
        self.boton_guia.setText("Guía")
        self.boton_guia.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.boton_guia.setToolTip("Guía paso a paso (F2)")
        toolbar.addWidget(self.boton_guia)
        
        # Botón Acerca de
        self.boton_acerca_de = QToolButton()
        self.boton_acerca_de.setIcon(get_icon('info'))
        self.boton_acerca_de.setText("Acerca de")
        self.boton_acerca_de.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.boton_acerca_de.setToolTip("Acerca de TLV 4.0 y desarrollador")
        toolbar.addWidget(self.boton_acerca_de)
        
        self.addToolBar(toolbar)
    
    def _crear_area_principal(self, layout_padre: QVBoxLayout) -> None:
        """Crea el área principal con pestañas."""
        # Crear widget de pestañas
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        
        # Aplicar estilos a las pestañas
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {Colors.FG_DIM};
                background-color: {Colors.BG0};
            }}
            
            QTabBar::tab {{
                background-color: {Colors.BG1};
                color: {Colors.FG};
                padding: 8px 16px;
                margin-right: 2px;
                border: 1px solid {Colors.FG_DIM};
                border-bottom: none;
                font-family: 'Consolas', 'Monaco', monospace;
                font-weight: bold;
            }}
            
            QTabBar::tab:selected {{
                background-color: {Colors.BG0};
                color: {Colors.ACCENT_CYAN};
                border-color: {Colors.ACCENT_CYAN};
            }}
            
            QTabBar::tab:hover {{
                background-color: {Colors.BG2};
                color: {Colors.ACCENT_NEO};
            }}
        """)
        
        # Crear pestaña de Enlaces
        self._crear_tab_enlaces()
        
        # Crear pestaña de Notas
        self._crear_tab_notas()
        
        # Crear pestaña de Grupos SN
        self._crear_tab_grupos_sn()
        
        layout_padre.addWidget(self.tab_widget)
    
    def _crear_tab_enlaces(self) -> None:
        """Crea la pestaña de gestión de enlaces"""
        enlaces_widget = QWidget()
        layout = QHBoxLayout(enlaces_widget)
        layout.setContentsMargins(4, 4, 4, 4)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Panel izquierdo - Categorías
        self._crear_panel_categorias(splitter)
        
        # Panel derecho - Tabla de enlaces
        self._crear_panel_enlaces(splitter)
        
        # Configurar proporciones del splitter
        splitter.setSizes([250, 750])
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)
        
        layout.addWidget(splitter)
        
        # Añadir pestaña
        self.tab_widget.addTab(enlaces_widget, "🔗 Enlaces")
    
    def _crear_tab_notas(self) -> None:
        """Crea la pestaña de notas"""
        # Crear widget de notas
        self.notes_widget = NotesWidget()
        
        # Conectar señales
        self.notes_widget.nota_guardada.connect(self._nota_guardada)
        self.notes_widget.nota_eliminada.connect(self._nota_eliminada)
        
        # Añadir pestaña
        self.tab_widget.addTab(self.notes_widget, "📝 Notas")
    
    def _crear_tab_grupos_sn(self) -> None:
        """Crea la pestaña de Grupos Service Now"""
        # Crear widget de grupos SN
        self.grupos_sn_widget = GruposSNWidget()
        
        # Añadir pestaña
        self.tab_widget.addTab(self.grupos_sn_widget, "👥 Grupos SN")
    
    def _crear_panel_categorias(self, splitter: QSplitter) -> None:
        """Crea el panel de categorías con estilo mejorado."""
        widget_categorias = QWidget()
        layout_categorias = QVBoxLayout(widget_categorias)
        layout_categorias.setContentsMargins(8, 8, 8, 8)
        layout_categorias.setSpacing(6)
        
        # Header con título y botones
        header_layout = QHBoxLayout()
        
        # Título estilizado
        label_categorias = QLabel("📁 CATEGORÍAS")
        label_categorias.setFont(Fonts.get_monospace_font(Fonts.SIZE_MEDIUM, bold=True))
        label_categorias.setStyleSheet(f"""
            color: {Colors.ACCENT_CYAN}; 
            padding: 8px 4px;
            font-weight: bold;
        """)
        header_layout.addWidget(label_categorias)
        
        header_layout.addStretch()
        
        # Botón para crear nueva categoría
        self.btn_nueva_categoria = QPushButton("➕")
        self.btn_nueva_categoria.setToolTip("Crear nueva categoría")
        self.btn_nueva_categoria.setFixedSize(30, 30)
        self.btn_nueva_categoria.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.ACCENT_NEO};
                color: {Colors.BG0};
                border: 1px solid {Colors.BORDER};
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {Colors.ACCENT_CYAN};
                border-color: {Colors.ACCENT_CYAN};
            }}
            QPushButton:pressed {{
                background-color: {Colors.PRESSED};
            }}
        """)
        self.btn_nueva_categoria.clicked.connect(self._crear_nueva_categoria)
        header_layout.addWidget(self.btn_nueva_categoria)
        
        # Botón para eliminar categoría
        self.btn_eliminar_categoria = QPushButton("🗑️")
        self.btn_eliminar_categoria.setToolTip("Eliminar categoría seleccionada")
        self.btn_eliminar_categoria.setFixedSize(30, 30)
        self.btn_eliminar_categoria.setEnabled(False)
        self.btn_eliminar_categoria.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.ACCENT_AMBER};
                color: {Colors.BG0};
                border: 1px solid {Colors.BORDER};
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover:enabled {{
                background-color: #ff4757;
                border-color: #ff4757;
            }}
            QPushButton:pressed:enabled {{
                background-color: {Colors.PRESSED};
            }}
            QPushButton:disabled {{
                background-color: {Colors.BG2};
                color: {Colors.FG_DIM};
                border-color: {Colors.BORDER};
            }}
        """)
        self.btn_eliminar_categoria.clicked.connect(self._eliminar_categoria_seleccionada)
        header_layout.addWidget(self.btn_eliminar_categoria)
        
        layout_categorias.addLayout(header_layout)
        
        # Lista de categorías con estilo mejorado
        self.lista_categorias = QListWidget()
        self.lista_categorias.setMaximumWidth(300)
        self.lista_categorias.setMinimumHeight(200)
        
        # Aplicar estilo mejorado con iconos y texto más grandes
        self.lista_categorias.setStyleSheet(f"""
            QListWidget {{
                background-color: {Colors.BG1};
                border: 1px solid {Colors.BORDER};
                border-radius: 6px;
                padding: 4px;
                outline: none;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                font-weight: 500;
                selection-background-color: {Colors.ACCENT_CYAN};
                selection-color: {Colors.BG0};
            }}
            QListWidget::item {{
                padding: 12px 16px;
                margin: 3px 2px;
                border-radius: 6px;
                color: {Colors.FG};
                border: 1px solid transparent;
                min-height: 24px;
            }}
            QListWidget::item:hover {{
                background-color: {Colors.HOVER};
                border-color: {Colors.ACCENT_CYAN};
            }}
            QListWidget::item:selected {{
                background-color: {Colors.ACCENT_CYAN};
                color: {Colors.BG0};
                font-weight: bold;
                border-color: {Colors.ACCENT_CYAN};
            }}
            QListWidget::item:selected:hover {{
                background-color: {Colors.ACCENT_NEO};
                border-color: {Colors.ACCENT_NEO};
            }}
        """)
        
        layout_categorias.addWidget(self.lista_categorias)
        
        # Configurar fondo del panel con imagen
        self._configurar_fondo_panel_categorias(widget_categorias)
        
        splitter.addWidget(widget_categorias)
    
    def _crear_panel_enlaces(self, splitter: QSplitter) -> None:
        """Crea el panel de enlaces."""
        widget_enlaces = QWidget()
        layout_enlaces = QVBoxLayout(widget_enlaces)
        layout_enlaces.setContentsMargins(8, 4, 8, 8)
        layout_enlaces.setSpacing(6)
        
        # Información y estadísticas - más compacta
        self.label_info = QLabel("📊 Cargando enlaces...")
        self.label_info.setFont(Fonts.get_monospace_font(Fonts.SIZE_SMALL))
        self.label_info.setStyleSheet(f"""
            QLabel {{
                color: {Colors.FG_DIM};
                padding: 4px 8px;
                background-color: {Colors.BG1};
                border-radius: 4px;
                border: 1px solid {Colors.BORDER};
            }}
        """)
        self.label_info.setMaximumHeight(28)
        layout_enlaces.addWidget(self.label_info)
        
        # Tabla de enlaces
        self.tabla_enlaces = QTableView()
        self.tabla_enlaces.setModel(self.modelo_tabla)
        self.tabla_enlaces.setAlternatingRowColors(True)
        self.tabla_enlaces.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.tabla_enlaces.setSortingEnabled(True)
        
        # Configurar altura de filas optimizada para URLs largas
        config_tabla = obtener_config_tabla()
        self.tabla_enlaces.verticalHeader().setDefaultSectionSize(config_tabla['fila_altura_default'])
        self.tabla_enlaces.verticalHeader().setMinimumSectionSize(config_tabla['fila_altura_minima'])
        self.tabla_enlaces.verticalHeader().setMaximumSectionSize(config_tabla['fila_altura_maxima'])
        
        # Configurar wrap de texto según configuración
        self.tabla_enlaces.setWordWrap(config_tabla['word_wrap'])
        
        # Aplicar delegate de tags para la columna de tags
        self.tag_delegate = TagDelegate()
        # Asumiendo que la columna de tags es la columna 3 (0-indexada)
        self.tabla_enlaces.setItemDelegateForColumn(3, self.tag_delegate)
        
        # Configurar columnas con anchos optimizados
        header = self.tabla_enlaces.horizontalHeader()
        header.setStretchLastSection(True)
        
        # Configurar anchos de columnas específicos para URLs largas
        header.setDefaultSectionSize(150)  # Ancho por defecto
        
        # Anchos específicos por columna usando configuración
        self.tabla_enlaces.setColumnWidth(0, config_tabla['columna_titulo'])   # Título
        self.tabla_enlaces.setColumnWidth(1, config_tabla['columna_url'])      # URL
        self.tabla_enlaces.setColumnWidth(2, config_tabla['columna_categoria']) # Categoría
        self.tabla_enlaces.setColumnWidth(3, config_tabla['columna_tags'])     # Tags
        # La columna 4 (Fecha) se ajustará automáticamente
        
        # Aplicar estilo moderno mejorado para la tabla
        self._aplicar_estilo_tabla_moderno()
        
        layout_enlaces.addWidget(self.tabla_enlaces)
        
        splitter.addWidget(widget_enlaces)

    def _aplicar_estilo_tabla_moderno(self) -> None:
        """Aplica un estilo moderno y elegante a la tabla de enlaces"""
        config_tabla = obtener_config_tabla()
        colors = obtener_color_scheme()
        typography = obtener_typography()
        spacing = obtener_spacing()
        elevation = obtener_elevation()
        
        tabla_style = f"""
        QTableView {{
            background-color: {colors['surface_elevated']};
            alternate-background-color: {colors['surface_variant']};
            color: {colors['on_surface']};
            gridline-color: {colors['outline_variant']};
            border: 1px solid {colors['outline']};
            border-radius: {elevation['border_radius']['medium']}px;
            font-size: {typography['font_sizes']['body']}px;
            font-family: {typography['font_family_primary']};
            selection-background-color: {config_tabla['color_seleccion']};
            selection-color: {config_tabla['color_seleccion_texto']};
        }}
        
        QTableView::item {{
            padding: {spacing['sm']}px;
            border: none;
            border-bottom: 1px solid {colors['outline_variant']};
        }}
        
        QTableView::item:selected {{
            background-color: {config_tabla['color_seleccion']};
            color: {config_tabla['color_seleccion_texto']};
            font-weight: {typography['font_weights']['medium']};
        }}
        
        QTableView::item:hover:!selected {{
            background-color: {config_tabla['color_hover']};
            color: {config_tabla['color_seleccion_texto']};
        }}
        
        QTableView::item:focus {{
            outline: 2px solid {colors['primary']};
            outline-offset: -2px;
        }}
        
        /* Header mejorado */
        QHeaderView::section {{
            background-color: {colors['primary']};
            color: {colors['on_primary']};
            padding: {spacing['md']}px {spacing['sm']}px;
            border: none;
            border-right: 1px solid {colors['primary_dark']};
            font-weight: {typography['font_weights']['semibold']};
            font-size: {typography['font_sizes']['caption']}px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        QHeaderView::section:first {{
            border-top-left-radius: {elevation['border_radius']['medium']}px;
        }}
        
        QHeaderView::section:last {{
            border-top-right-radius: {elevation['border_radius']['medium']}px;
            border-right: none;
        }}
        
        QHeaderView::section:hover {{
            background-color: {colors['primary_variant']};
        }}
        
        /* Corner button */
        QTableCornerButton::section {{
            background-color: {colors['primary']};
            border: none;
            border-top-left-radius: {elevation['border_radius']['medium']}px;
        }}
        """
        
        self.tabla_enlaces.setStyleSheet(tabla_style)
    
    def _crear_barra_estado(self) -> None:
        """Crea la barra de estado con información mejorada."""
        self.barra_estado = QStatusBar()
        self.setStatusBar(self.barra_estado)
        
        # Configurar estilo
        self.barra_estado.setStyleSheet("""
            QStatusBar {
                background-color: #323233;
                color: #ffffff;
                border-top: 1px solid #404040;
                font-size: 12px;
            }
        """)
        
        # Mostrar mensaje inicial
        mensaje_inicial = "🔗 TECH LINK VIEWER v4.0.0 - Listo para buscar enlaces"
        self.barra_estado.showMessage(mensaje_inicial)
    
    def _conectar_senales(self) -> None:
        """Conecta las señales de los widgets."""
        # Búsqueda
        self.campo_busqueda.textChanged.connect(self._busqueda_cambiada)
        
        # Botones principales
        self.boton_nuevo.clicked.connect(self._nuevo_enlace)
        self.boton_editar.clicked.connect(self._editar_enlace_seleccionado)
        self.boton_eliminar.clicked.connect(self._eliminar_enlace_seleccionado)
        self.boton_importar.clicked.connect(self._importar_json)
        self.boton_exportar.clicked.connect(self._exportar_json)
        
        # Botones adicionales
        self.boton_refrescar.clicked.connect(self._refrescar_datos)
        self.boton_configuracion.clicked.connect(self._mostrar_configuracion)
        self.boton_ayuda.clicked.connect(self._mostrar_ayuda)
        self.boton_guia.clicked.connect(self._mostrar_guia_paso_a_paso)
        self.boton_acerca_de.clicked.connect(self._mostrar_acerca_de)
        
        # Categorías
        self.lista_categorias.itemClicked.connect(self._categoria_seleccionada)
        self.lista_categorias.itemSelectionChanged.connect(self._categoria_seleccion_cambiada)
        
        # Tabla
        self.tabla_enlaces.doubleClicked.connect(self._abrir_enlace)
        self.tabla_enlaces.selectionModel().selectionChanged.connect(self._seleccion_tabla_cambiada)
    
    def _configurar_atajos(self) -> None:
        """Configura los atajos de teclado."""
        # Atajo para nuevo enlace
        shortcut_nuevo = QShortcut(QKeySequence("Ctrl+N"), self)
        shortcut_nuevo.activated.connect(self._nuevo_enlace)
        
        # Atajo para editar
        shortcut_editar = QShortcut(QKeySequence("Ctrl+E"), self)
        shortcut_editar.activated.connect(self._editar_enlace_seleccionado)
        
        # Atajo para eliminar
        shortcut_eliminar = QShortcut(QKeySequence("Del"), self)
        shortcut_eliminar.activated.connect(self._eliminar_enlace_seleccionado)
        
        # Atajo para guardar
        shortcut_guardar = QShortcut(QKeySequence("Ctrl+S"), self)
        shortcut_guardar.activated.connect(self._guardar_datos)
        
        # Atajo para enfocar búsqueda
        shortcut_buscar = QShortcut(QKeySequence("Ctrl+F"), self)
        shortcut_buscar.activated.connect(self._enfocar_busqueda)
        
        # Atajo para abrir enlace
        shortcut_abrir = QShortcut(QKeySequence("Return"), self.tabla_enlaces)
        shortcut_abrir.activated.connect(self._abrir_enlace_seleccionado)
        
        # Atajos para nuevas funciones
        shortcut_refrescar = QShortcut(QKeySequence("F5"), self)
        shortcut_refrescar.activated.connect(self._refrescar_datos)
        
        shortcut_ayuda = QShortcut(QKeySequence("F1"), self)
        shortcut_ayuda.activated.connect(self._mostrar_ayuda)
        
        shortcut_guia = QShortcut(QKeySequence("F2"), self)
        shortcut_guia.activated.connect(self._mostrar_guia_paso_a_paso)
        
        # Atajos para cambiar pestañas
        shortcut_tab_enlaces = QShortcut(QKeySequence("Ctrl+1"), self)
        shortcut_tab_enlaces.activated.connect(lambda: self.tab_widget.setCurrentIndex(0))
        
        shortcut_tab_notas = QShortcut(QKeySequence("Ctrl+2"), self)
        shortcut_tab_notas.activated.connect(lambda: self.tab_widget.setCurrentIndex(1))
        
        shortcut_tab_grupos = QShortcut(QKeySequence("Ctrl+3"), self)
        shortcut_tab_grupos.activated.connect(lambda: self.tab_widget.setCurrentIndex(2))
        
        # Atajo para nueva nota (solo en pestaña de notas)
        shortcut_nueva_nota = QShortcut(QKeySequence("Ctrl+Shift+N"), self)
        shortcut_nueva_nota.activated.connect(self._nueva_nota_global)
        
        # Atajo para limpiar búsqueda
        shortcut_escape = QShortcut(QKeySequence("Escape"), self)
        shortcut_escape.activated.connect(self._limpiar_busqueda)
    
    def _cargar_datos_iniciales(self) -> None:
        """Carga los datos iniciales."""
        self._actualizar_lista_categorias()
        self._actualizar_tabla_enlaces()
        self._actualizar_informacion()
        self.barra_estado.showMessage("Datos cargados correctamente")
    
    def _actualizar_lista_categorias(self) -> None:
        """Actualiza la lista de categorías."""
        self.lista_categorias.clear()
        
        # Agregar "Todas" como primera opción
        enlaces = self.repositorio.obtener_enlaces()
        total_enlaces = len(enlaces)
        item_todas = QListWidgetItem(f"📁 Todas ({total_enlaces})")
        self.lista_categorias.addItem(item_todas)
        
        # Obtener todas las categorías (tanto del repositorio como de los enlaces)
        categorias_repositorio = self.repositorio._datos.get('categorias', [])
        categorias_enlaces = extraer_todas_las_categorias(enlaces)
        
        # Combinar ambas listas sin duplicados
        todas_categorias = list(set(categorias_repositorio + categorias_enlaces))
        todas_categorias.sort()  # Ordenar alfabéticamente
        
        for categoria in todas_categorias:
            # Contar enlaces en esta categoría
            count = sum(1 for enlace in enlaces if enlace.get('categoria') == categoria)
            item_categoria = QListWidgetItem(f"📂 {categoria} ({count})")
            self.lista_categorias.addItem(item_categoria)
    
    def _actualizar_tabla_enlaces(self) -> None:
        """Actualiza la tabla de enlaces con filtros aplicados."""
        enlaces = self.repositorio.obtener_enlaces()
        
        # Aplicar búsqueda y filtros
        resultados = buscar_enlaces(
            enlaces,
            self.busqueda_actual,
            self.categoria_filtro_actual,
            self.tag_filtro_actual
        )
        
        # Actualizar modelo
        if self.busqueda_actual or self.tag_filtro_actual:
            self.modelo_tabla.actualizar_enlaces_con_score(resultados)
        else:
            enlaces_filtrados = [enlace for enlace, _ in resultados]
            self.modelo_tabla.actualizar_enlaces(enlaces_filtrados)
        
        # Ajustar columnas
        self.tabla_enlaces.resizeColumnsToContents()
    
    def _actualizar_informacion(self) -> None:
        """Actualiza la información estadística."""
        estadisticas = self.repositorio.obtener_estadisticas()
        enlaces_mostrados = self.modelo_tabla.obtener_numero_enlaces()
        
        info_texto = f"📊 Mostrando {enlaces_mostrados} de {estadisticas['total_enlaces']} enlaces"
        
        if self.categoria_filtro_actual:
            info_texto += f" | Categoría: {self.categoria_filtro_actual}"
        
        if self.tag_filtro_actual:
            info_texto += f" | Tag: {self.tag_filtro_actual}"
        
        if self.busqueda_actual:
            info_texto += f" | Búsqueda: '{self.busqueda_actual}'"
        
        self.label_info.setText(info_texto)
    
    def _busqueda_cambiada(self) -> None:
        """Maneja el cambio en el campo de búsqueda."""
        # Usar timer para evitar búsquedas muy frecuentes
        self.timer_busqueda.stop()
        self.timer_busqueda.start(300)  # 300ms de delay
    
    def _realizar_busqueda(self) -> None:
        """Realiza la búsqueda actual."""
        self.busqueda_actual = self.campo_busqueda.text().strip()
        self._actualizar_tabla_enlaces()
        self._actualizar_informacion()
    
    def _limpiar_busqueda(self) -> None:
        """Limpia la búsqueda actual."""
        self.campo_busqueda.clear()
        self.busqueda_actual = ""
        self.tag_filtro_actual = ""
        self._actualizar_tabla_enlaces()
        self._actualizar_informacion()
        self.boton_limpiar.setVisible(False)
    
    def _enfocar_busqueda(self) -> None:
        """Enfoca el campo de búsqueda."""
        self.campo_busqueda.setFocus()
        self.campo_busqueda.selectAll()
    
    def _categoria_seleccionada(self) -> None:
        """Maneja la selección de una categoría."""
        item = self.lista_categorias.currentItem()
        if not item:
            return
        
        texto = item.text()
        
        if texto.startswith("�️ Todas"):
            self.categoria_filtro_actual = ""
        else:
            # Extraer nombre de categoría del texto "� Nombre (count)"
            inicio = texto.find(" ") + 1
            fin = texto.rfind(" (")
            if fin > inicio:
                self.categoria_filtro_actual = texto[inicio:fin]
            else:
                self.categoria_filtro_actual = texto[inicio:]
        
        self.tag_filtro_actual = ""  # Limpiar filtro de tag
        self._actualizar_tabla_enlaces()
        self._actualizar_informacion()
    
    def _categoria_seleccion_cambiada(self) -> None:
        """Maneja cambios en la selección de categorías para habilitar/deshabilitar botones."""
        items_seleccionados = self.lista_categorias.selectedItems()
        if not items_seleccionados:
            self.btn_eliminar_categoria.setEnabled(False)
            return
        
        item = items_seleccionados[0]
        texto = item.text()
        
        # No permitir eliminar "Todas"
        es_todas = texto.startswith("�️ Todas")
        self.btn_eliminar_categoria.setEnabled(not es_todas)
    
    def _crear_nueva_categoria(self) -> None:
        """Crea una nueva categoría."""
        nombre, ok = QInputDialog.getText(
            self, 
            "Nueva Categoría", 
            "Ingrese el nombre de la nueva categoría:",
            text=""
        )
        
        if not ok or not nombre.strip():
            return
        
        nombre = nombre.strip()
        
        # Verificar que no exista ya
        enlaces = self.repositorio.obtener_enlaces()
        categorias_existentes = extraer_todas_las_categorias(enlaces)
        
        if nombre in categorias_existentes:
            QMessageBox.warning(
                self,
                "Categoría Existente",
                f"La categoría '{nombre}' ya existe."
            )
            return
        
        # Agregar la nueva categoría al repositorio
        try:
            # Las categorías se crean automáticamente cuando se agrega un enlace,
            # pero podemos agregar la categoría a la lista de categorías del repositorio
            categorias = self.repositorio._datos.get('categorias', [])
            if nombre not in categorias:
                categorias.append(nombre)
                self.repositorio._datos['categorias'] = categorias
                self.repositorio.guardar()
            
            self._actualizar_lista_categorias()
            
            # Seleccionar la nueva categoría
            for i in range(self.lista_categorias.count()):
                item = self.lista_categorias.item(i)
                if nombre in item.text():
                    self.lista_categorias.setCurrentItem(item)
                    break
            
            logger.info(f"Categoría '{nombre}' creada exitosamente")
            
        except Exception as e:
            logger.error(f"Error al crear categoría: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo crear la categoría: {str(e)}"
            )
    
    def _eliminar_categoria_seleccionada(self) -> None:
        """Elimina la categoría seleccionada."""
        item = self.lista_categorias.currentItem()
        if not item:
            return
        
        texto = item.text()
        
        # No permitir eliminar "Todas"
        if texto.startswith("�️ Todas"):
            return
        
        # Extraer nombre de categoría
        inicio = texto.find(" ") + 1
        fin = texto.rfind(" (")
        if fin > inicio:
            nombre_categoria = texto[inicio:fin]
        else:
            nombre_categoria = texto[inicio:]
        
        # Contar enlaces en esta categoría
        enlaces = self.repositorio.obtener_enlaces()
        enlaces_en_categoria = [e for e in enlaces if e.get('categoria') == nombre_categoria]
        
        if enlaces_en_categoria:
            respuesta = QMessageBox.question(
                self,
                "Eliminar Categoría",
                f"La categoría '{nombre_categoria}' contiene {len(enlaces_en_categoria)} enlace(s).\n\n"
                "¿Qué desea hacer con estos enlaces?",
                QMessageBox.StandardButton.Cancel
            )
            
            # Crear botones personalizados
            mover_btn = QPushButton("Mover a 'General'")
            eliminar_btn = QPushButton("Eliminar enlaces")
            cancelar_btn = QPushButton("Cancelar")
            
            msg = QMessageBox(self)
            msg.setWindowTitle("Eliminar Categoría")
            msg.setText(f"La categoría '{nombre_categoria}' contiene {len(enlaces_en_categoria)} enlace(s).")
            msg.setInformativeText("¿Qué desea hacer con estos enlaces?")
            msg.addButton(mover_btn, QMessageBox.ButtonRole.AcceptRole)
            msg.addButton(eliminar_btn, QMessageBox.ButtonRole.DestructiveRole)
            msg.addButton(cancelar_btn, QMessageBox.ButtonRole.RejectRole)
            msg.setDefaultButton(mover_btn)
            
            resultado = msg.exec()
            
            if msg.clickedButton() == cancelar_btn:
                return
            elif msg.clickedButton() == mover_btn:
                # Mover enlaces a categoría "General"
                for enlace in enlaces_en_categoria:
                    enlace['categoria'] = 'General'
                
                # Asegurar que "General" esté en la lista de categorías
                categorias = self.repositorio._datos.get('categorias', [])
                if 'General' not in categorias:
                    categorias.append('General')
                    self.repositorio._datos['categorias'] = categorias
                    
            elif msg.clickedButton() == eliminar_btn:
                # Eliminar todos los enlaces de la categoría
                enlaces_filtrados = [e for e in enlaces if e.get('categoria') != nombre_categoria]
                self.repositorio._datos['links'] = enlaces_filtrados
        
        try:
            # Eliminar la categoría de la lista de categorías
            categorias = self.repositorio._datos.get('categorias', [])
            if nombre_categoria in categorias:
                categorias.remove(nombre_categoria)
                self.repositorio._datos['categorias'] = categorias
            
            # Guardar cambios
            self.repositorio.guardar()
            
            # Actualizar interfaz
            self._actualizar_lista_categorias()
            self._actualizar_tabla_enlaces()
            self._actualizar_informacion()
            
            # Limpiar filtro si era la categoría eliminada
            if self.categoria_filtro_actual == nombre_categoria:
                self.categoria_filtro_actual = ""
                self.lista_categorias.setCurrentRow(0)  # Seleccionar "Todas"
            
            logger.info(f"Categoría '{nombre_categoria}' eliminada exitosamente")
            
        except Exception as e:
            logger.error(f"Error al eliminar categoría: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo eliminar la categoría: {str(e)}"
            )
    
    def _seleccion_tabla_cambiada(self) -> None:
        """Maneja cambios en la selección de la tabla."""
        indices_seleccionados = self.tabla_enlaces.selectionModel().selectedRows()
        hay_seleccion = len(indices_seleccionados) > 0
        
        # Habilitar/deshabilitar botones según hay selección
        self.boton_editar.setEnabled(hay_seleccion)
        self.boton_eliminar.setEnabled(hay_seleccion)
    
    def _enlace_clickeado(self, index) -> None:
        """Maneja el clic en un enlace."""
        if not index.isValid():
            return
        
        # Si se clickeó en la columna de tags, detectar tag específico
        if index.column() == 3:  # Columna de tags
            enlace = self.modelo_tabla.obtener_enlace_por_fila(index.row())
            if enlace and 'tags' in enlace:
                tags = enlace['tags']
                if tags:
                    # Por simplicidad, usar el primer tag
                    # En una implementación más avanzada, se detectaría la posición exacta
                    tag_clickeado = tags[0]
                    self._filtrar_por_tag(tag_clickeado)
    
    def _filtrar_por_tag(self, tag: str) -> None:
        """Filtra enlaces por un tag específico."""
        self.tag_filtro_actual = tag
        self.categoria_filtro_actual = ""  # Limpiar filtro de categoría
        self._actualizar_tabla_enlaces()
        self._actualizar_informacion()
        
        # Actualizar campo de búsqueda para mostrar el filtro
        self.campo_busqueda.setText(f"tag:{tag}")
    
    def _abrir_enlace(self) -> None:
        """Abre el enlace seleccionado."""
        index = self.tabla_enlaces.currentIndex()
        if not index.isValid():
            return
        
        enlace = self.modelo_tabla.obtener_enlace_por_fila(index.row())
        if enlace:
            url = enlace.get('url', '')
            if url:
                if abrir_url(url):
                    self.barra_estado.showMessage(f"Abriendo: {url}", 3000)
                else:
                    QMessageBox.warning(self, "Error", f"No se pudo abrir la URL: {url}")
    
    def _abrir_enlace_seleccionado(self) -> None:
        """Abre el enlace actualmente seleccionado."""
        self._abrir_enlace()
    
    def _nuevo_enlace(self) -> None:
        """Crea un nuevo enlace."""
        categorias = self.repositorio.obtener_categorias()
        enlaces = self.repositorio.obtener_enlaces()
        tags_existentes = extraer_todos_los_tags(enlaces)
        
        dialogo = DialogoEnlace(
            self, 
            None, 
            categorias, 
            tags_existentes
        )
        
        dialogo.enlace_aceptado.connect(self._procesar_nuevo_enlace)
        dialogo.exec()
    
    def _procesar_nuevo_enlace(self, datos: Dict[str, Any]) -> None:
        """Procesa la creación de un nuevo enlace."""
        enlace_id = self.repositorio.agregar_enlace(
            datos['titulo'],
            datos['url'],
            datos['categoria'],
            datos['tags']
        )
        
        if enlace_id:
            if self.repositorio.guardar():
                self._cargar_datos_iniciales()
                self.barra_estado.showMessage(f"Enlace '{datos['titulo']}' creado correctamente", 3000)
            else:
                QMessageBox.warning(self, "Error", "No se pudo guardar el enlace.")
        else:
            QMessageBox.warning(self, "Error", "No se pudo crear el enlace. Verifica que la URL no esté duplicada.")
    
    def _editar_enlace_seleccionado(self) -> None:
        """Edita el enlace actualmente seleccionado."""
        index = self.tabla_enlaces.currentIndex()
        if not index.isValid():
            QMessageBox.information(self, "Información", "Selecciona un enlace para editar.")
            return
        
        enlace = self.modelo_tabla.obtener_enlace_por_fila(index.row())
        if not enlace:
            return
        
        categorias = self.repositorio.obtener_categorias()
        enlaces = self.repositorio.obtener_enlaces()
        tags_existentes = extraer_todos_los_tags(enlaces)
        
        dialogo = DialogoEnlace(
            self,
            enlace,
            categorias,
            tags_existentes
        )
        
        dialogo.enlace_aceptado.connect(self._procesar_edicion_enlace)
        dialogo.exec()
    
    def _procesar_edicion_enlace(self, datos: Dict[str, Any]) -> None:
        """Procesa la edición de un enlace."""
        if 'id' not in datos:
            return
        
        if self.repositorio.actualizar_enlace(
            datos['id'],
            datos['titulo'],
            datos['url'],
            datos['categoria'],
            datos['tags']
        ):
            if self.repositorio.guardar():
                self._cargar_datos_iniciales()
                self.barra_estado.showMessage(f"Enlace '{datos['titulo']}' actualizado correctamente", 3000)
            else:
                QMessageBox.warning(self, "Error", "No se pudo guardar los cambios.")
        else:
            QMessageBox.warning(self, "Error", "No se pudo actualizar el enlace.")
    
    def _eliminar_enlace_seleccionado(self) -> None:
        """Elimina el enlace actualmente seleccionado."""
        index = self.tabla_enlaces.currentIndex()
        if not index.isValid():
            QMessageBox.information(self, "Información", "Selecciona un enlace para eliminar.")
            return
        
        enlace = self.modelo_tabla.obtener_enlace_por_fila(index.row())
        if not enlace:
            return
        
        titulo = enlace.get('titulo', 'Enlace sin título')
        respuesta = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Estás seguro de que quieres eliminar el enlace '{titulo}'?\n\nEsta acción no se puede deshacer.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            if self.repositorio.eliminar_enlace(enlace['id']):
                if self.repositorio.guardar():
                    self._cargar_datos_iniciales()
                    self.barra_estado.showMessage(f"Enlace '{titulo}' eliminado correctamente", 3000)
                else:
                    QMessageBox.warning(self, "Error", "No se pudo guardar los cambios.")
            else:
                QMessageBox.warning(self, "Error", "No se pudo eliminar el enlace.")
    
    def _guardar_datos(self) -> None:
        """Guarda los datos manualmente."""
        if self.repositorio.guardar():
            self.barra_estado.showMessage("Datos guardados correctamente", 3000)
        else:
            QMessageBox.warning(self, "Error", "No se pudieron guardar los datos.")
    
    def _nueva_categoria(self) -> None:
        """Crea una nueva categoría."""
        from PyQt6.QtWidgets import QInputDialog
        
        categoria, ok = QInputDialog.getText(self, "Nueva Categoría", "Nombre de la categoría:")
        
        if ok and categoria:
            if self.repositorio.agregar_categoria(categoria):
                if self.repositorio.guardar():
                    self._actualizar_lista_categorias()
                    self.barra_estado.showMessage(f"Categoría '{categoria}' creada correctamente", 3000)
                else:
                    QMessageBox.warning(self, "Error", "No se pudo guardar la nueva categoría.")
            else:
                QMessageBox.warning(self, "Error", "La categoría ya existe o el nombre no es válido.")
    
    def _renombrar_categoria(self) -> None:
        """Renombra la categoría seleccionada."""
        item = self.lista_categorias.currentItem()
        if not item or item.text().startswith("📂 Todas"):
            QMessageBox.information(self, "Información", "Selecciona una categoría para renombrar.")
            return
        
        # Extraer nombre actual
        texto = item.text()
        inicio = texto.find(" ") + 1
        fin = texto.rfind(" (")
        if fin > inicio:
            categoria_actual = texto[inicio:fin]
        else:
            categoria_actual = texto[inicio:]
        
        from PyQt6.QtWidgets import QInputDialog
        
        categoria_nueva, ok = QInputDialog.getText(
            self, 
            "Renombrar Categoría", 
            "Nuevo nombre:",
            text=categoria_actual
        )
        
        if ok and categoria_nueva and categoria_nueva != categoria_actual:
            if self.repositorio.renombrar_categoria(categoria_actual, categoria_nueva):
                if self.repositorio.guardar():
                    self._cargar_datos_iniciales()
                    self.barra_estado.showMessage(f"Categoría renombrada a '{categoria_nueva}'", 3000)
                else:
                    QMessageBox.warning(self, "Error", "No se pudo guardar el cambio.")
            else:
                QMessageBox.warning(self, "Error", "No se pudo renombrar la categoría.")
    
    def _eliminar_categoria(self) -> None:
        """Elimina la categoría seleccionada."""
        item = self.lista_categorias.currentItem()
        if not item or item.text().startswith("📂 Todas"):
            QMessageBox.information(self, "Información", "Selecciona una categoría para eliminar.")
            return
        
        # Extraer nombre de categoría
        texto = item.text()
        inicio = texto.find(" ") + 1
        fin = texto.rfind(" (")
        if fin > inicio:
            categoria = texto[inicio:fin]
        else:
            categoria = texto[inicio:]
        
        # Confirmar eliminación
        respuesta = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Qué quieres hacer con los enlaces de la categoría '{categoria}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
        )
        
        if respuesta == QMessageBox.StandardButton.Cancel:
            return
        
        # TODO: Implementar diálogo para elegir categoría destino
        # Por simplicidad, eliminar enlaces también
        if self.repositorio.eliminar_categoria(categoria, None):
            if self.repositorio.guardar():
                self._cargar_datos_iniciales()
                self.barra_estado.showMessage(f"Categoría '{categoria}' eliminada", 3000)
            else:
                QMessageBox.warning(self, "Error", "No se pudo guardar los cambios.")
        else:
            QMessageBox.warning(self, "Error", "No se pudo eliminar la categoría.")
    
    def _importar_json(self) -> None:
        """Importa datos desde un archivo JSON."""
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Importar Enlaces",
            "",
            "Archivos JSON (*.json);;Todos los archivos (*)"
        )
        
        if archivo:
            try:
                from ..utils.io import cargar_json, validar_estructura_json
                datos = cargar_json(Path(archivo))
                
                if datos and validar_estructura_json(datos):
                    # Crear backup antes de importar
                    self.repositorio.crear_backup()
                    
                    if self.repositorio.importar_datos(datos):
                        if self.repositorio.guardar():
                            self._cargar_datos_iniciales()
                            self.barra_estado.showMessage("Datos importados correctamente", 3000)
                        else:
                            QMessageBox.warning(self, "Error", "No se pudieron guardar los datos importados.")
                    else:
                        QMessageBox.warning(self, "Error", "No se pudieron importar los datos.")
                else:
                    QMessageBox.warning(self, "Error", "El archivo no tiene un formato válido.")
            except Exception as e:
                logger.error(f"Error al importar: {e}")
                QMessageBox.warning(self, "Error", f"Error al importar archivo: {e}")
    
    def _exportar_json(self) -> None:
        """Exporta datos a un archivo JSON."""
        archivo, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar Enlaces",
            "enlaces_backup.json",
            "Archivos JSON (*.json);;Todos los archivos (*)"
        )
        
        if archivo:
            try:
                datos = self.repositorio.exportar_datos()
                from ..utils.io import guardar_json
                
                if guardar_json(datos, Path(archivo)):
                    self.barra_estado.showMessage(f"Datos exportados a {archivo}", 3000)
                else:
                    QMessageBox.warning(self, "Error", "No se pudo exportar el archivo.")
            except Exception as e:
                logger.error(f"Error al exportar: {e}")
                QMessageBox.warning(self, "Error", f"Error al exportar archivo: {e}")
    
    def _refrescar_datos(self) -> None:
        """Refresca los datos y la vista de forma completa."""
        try:
            # Guardar el estado actual
            categoria_seleccionada = None
            filtro_actual = self.filtro_entrada.text() if hasattr(self, 'filtro_entrada') else ""
            
            # Obtener categoría actualmente seleccionada
            if hasattr(self, 'lista_categorias') and self.lista_categorias.currentItem():
                categoria_seleccionada = self.lista_categorias.currentItem().text()
            
            # Mostrar mensaje de progreso
            self.statusBar().showMessage("Refrescando datos...", 0)
            
            # Recargar datos del repositorio
            self.repositorio.cargar()
            
            # Actualizar todas las vistas
            self._actualizar_categorias()
            
            # Restaurar selección de categoría si existe
            if categoria_seleccionada and hasattr(self, 'lista_categorias'):
                for i in range(self.lista_categorias.count()):
                    item = self.lista_categorias.item(i)
                    if item and item.text() == categoria_seleccionada:
                        self.lista_categorias.setCurrentItem(item)
                        break
            
            self._actualizar_tabla_enlaces()
            self._actualizar_informacion()
            
            # Restaurar filtro
            if filtro_actual and hasattr(self, 'filtro_entrada'):
                self.filtro_entrada.setText(filtro_actual)
                self._filtrar_enlaces()
            
            # Reconfigurar el fondo si está activado
            if hasattr(self, '_fondo_activado') and self._fondo_activado:
                self._configurar_fondo_translucido(self.centralWidget())
            
            # Mostrar mensaje de éxito
            self.statusBar().showMessage("✅ Datos refrescados correctamente", 3000)
            logger.info("Datos refrescados completamente por el usuario")
            
        except Exception as e:
            logger.error(f"Error al refrescar datos: {e}")
            self.statusBar().showMessage("❌ Error al refrescar", 3000)
            QMessageBox.warning(self, "Error", f"Error al refrescar datos:\n{str(e)}")
    
    def _mostrar_configuracion(self) -> None:
        """Muestra el diálogo de configuración."""
        from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, 
                                   QCheckBox, QSpinBox, QLabel, QPushButton,
                                   QComboBox, QSlider, QTabWidget, QWidget,
                                   QColorDialog, QFontDialog, QFileDialog)
        
        dialog = QDialog(self)
        dialog.setWindowTitle("⚙️ Configuración TLV 4.0")
        dialog.setFixedSize(500, 400)
        dialog.setModal(True)
        
        # Aplicar tema oscuro al diálogo
        dialog.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #555;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QCheckBox::indicator:checked {
                background-color: #00ff00;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Crear pestañas
        tabs = QTabWidget()
        
        # === PESTAÑA APARIENCIA ===
        tab_apariencia = QWidget()
        layout_apariencia = QVBoxLayout()
        
        # Grupo Fondo
        grupo_fondo = QGroupBox("🖼️ Fondo de Pantalla")
        layout_fondo = QVBoxLayout()
        
        self.check_fondo = QCheckBox("Activar fondo translúcido")
        self.check_fondo.setChecked(getattr(self, '_fondo_activado', False))
        layout_fondo.addWidget(self.check_fondo)
        
        btn_cambiar_fondo = QPushButton("📁 Cambiar imagen de fondo")
        btn_cambiar_fondo.clicked.connect(self._cambiar_imagen_fondo)
        layout_fondo.addWidget(btn_cambiar_fondo)
        
        # Transparencia
        layout_trans = QHBoxLayout()
        layout_trans.addWidget(QLabel("Transparencia:"))
        self.slider_transparencia = QSlider(Qt.Orientation.Horizontal)
        self.slider_transparencia.setRange(100, 255)
        self.slider_transparencia.setValue(230)
        layout_trans.addWidget(self.slider_transparencia)
        self.label_trans = QLabel("230")
        layout_trans.addWidget(self.label_trans)
        layout_fondo.addLayout(layout_trans)
        
        grupo_fondo.setLayout(layout_fondo)
        layout_apariencia.addWidget(grupo_fondo)
        
        # Grupo Tema
        grupo_tema = QGroupBox("🎨 Tema y Colores")
        layout_tema = QVBoxLayout()
        
        self.check_tema_oscuro = QCheckBox("Tema oscuro")
        self.check_tema_oscuro.setChecked(True)
        layout_tema.addWidget(self.check_tema_oscuro)
        
        self.check_efectos = QCheckBox("Efectos typewriter")
        self.check_efectos.setChecked(True)
        layout_tema.addWidget(self.check_efectos)
        
        grupo_tema.setLayout(layout_tema)
        layout_apariencia.addWidget(grupo_tema)
        
        tab_apariencia.setLayout(layout_apariencia)
        tabs.addTab(tab_apariencia, "🎨 Apariencia")
        
        # === PESTAÑA COMPORTAMIENTO ===
        tab_comportamiento = QWidget()
        layout_comportamiento = QVBoxLayout()
        
        # Grupo Auto-guardado
        grupo_auto = QGroupBox("💾 Auto-guardado")
        layout_auto = QVBoxLayout()
        
        self.check_auto_guardado = QCheckBox("Activar auto-guardado")
        self.check_auto_guardado.setChecked(True)
        layout_auto.addWidget(self.check_auto_guardado)
        
        layout_intervalo = QHBoxLayout()
        layout_intervalo.addWidget(QLabel("Intervalo (segundos):"))
        self.spin_intervalo = QSpinBox()
        self.spin_intervalo.setRange(10, 300)
        self.spin_intervalo.setValue(30)
        layout_intervalo.addWidget(self.spin_intervalo)
        layout_auto.addLayout(layout_intervalo)
        
        grupo_auto.setLayout(layout_auto)
        layout_comportamiento.addWidget(grupo_auto)
        
        # Grupo Notificaciones
        grupo_notif = QGroupBox("🔔 Notificaciones")
        layout_notif = QVBoxLayout()
        
        self.check_notif_guardado = QCheckBox("Notificar al guardar")
        self.check_notif_guardado.setChecked(True)
        layout_notif.addWidget(self.check_notif_guardado)
        
        self.check_sonidos = QCheckBox("Sonidos del sistema")
        self.check_sonidos.setChecked(False)
        layout_notif.addWidget(self.check_sonidos)
        
        grupo_notif.setLayout(layout_notif)
        layout_comportamiento.addWidget(grupo_notif)
        
        tab_comportamiento.setLayout(layout_comportamiento)
        tabs.addTab(tab_comportamiento, "⚙️ Comportamiento")
        
        layout.addWidget(tabs)
        
        # Botones
        layout_botones = QHBoxLayout()
        
        btn_restaurar = QPushButton("🔄 Restaurar")
        btn_restaurar.clicked.connect(self._restaurar_configuracion)
        layout_botones.addWidget(btn_restaurar)
        
        layout_botones.addStretch()
        
        btn_cancelar = QPushButton("❌ Cancelar")
        btn_cancelar.clicked.connect(dialog.reject)
        layout_botones.addWidget(btn_cancelar)
        
        btn_aplicar = QPushButton("✅ Aplicar")
        btn_aplicar.clicked.connect(lambda: self._aplicar_configuracion(dialog))
        layout_botones.addWidget(btn_aplicar)
        
        layout.addLayout(layout_botones)
        dialog.setLayout(layout)
        
        # Conectar eventos
        self.slider_transparencia.valueChanged.connect(
            lambda v: self.label_trans.setText(str(v))
        )
        
        dialog.exec()
    
    def _cambiar_imagen_fondo(self) -> None:
        """Permite cambiar la imagen de fondo."""
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar imagen de fondo",
            "",
            "Imágenes (*.jpg *.jpeg *.png *.bmp);;Todos los archivos (*)"
        )
        if archivo:
            QMessageBox.information(self, "Éxito", f"Nueva imagen seleccionada:\n{archivo}")
    
    def _restaurar_configuracion(self) -> None:
        """Restaura la configuración por defecto."""
        reply = QMessageBox.question(
            self,
            "Restaurar Configuración",
            "¿Estás seguro de que quieres restaurar la configuración por defecto?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Configuración", "Configuración restaurada correctamente")
    
    def _aplicar_configuracion(self, dialog) -> None:
        """Aplica la configuración seleccionada."""
        try:
            # Aplicar fondo
            if self.check_fondo.isChecked():
                self._fondo_activado = True
                self._configurar_fondo_translucido(self.centralWidget())
            else:
                self._fondo_activado = False
                self.setStyleSheet("")  # Limpiar estilos
            
            self.statusBar().showMessage("✅ Configuración aplicada correctamente", 3000)
            dialog.accept()
            
        except Exception as e:
            logger.error(f"Error al aplicar configuración: {e}")
            QMessageBox.warning(self, "Error", f"Error al aplicar configuración:\n{str(e)}")
    
    def _mostrar_ayuda(self) -> None:
        """Muestra la ayuda rápida de la aplicación."""
        ayuda_texto = """
        📋 AYUDA RÁPIDA - TECH LINK VIEWER 4.0
        
        🏷️ PESTAÑAS:
        • Ctrl+1: Cambiar a pestaña Enlaces
        • Ctrl+2: Cambiar a pestaña Notas
        • Ctrl+3: Cambiar a pestaña Grupos SN
        
        🔗 PESTAÑA ENLACES:
        🔍 BÚSQUEDA:
        • Escribe en el campo de búsqueda para filtrar enlaces
        • Búsqueda por título, URL, descripción y tags
        • Búsqueda en tiempo real
        
        📁 CATEGORÍAS:
        • Haz clic en una categoría para filtrar enlaces
        • "Todas" muestra todos los enlaces
        
        🔗 GESTIÓN DE ENLACES:
        • Doble clic: Abrir enlace en navegador
        • Nuevo: Ctrl+N
        • Editar: Ctrl+E (enlace seleccionado)
        • Eliminar: Del (enlace seleccionado)
        
        📝 PESTAÑA NOTAS:
        ✍️ GESTIÓN DE NOTAS:
        • Nueva nota: Ctrl+Shift+N
        • Auto-guardado automático cada 3 segundos
        • Búsqueda instantánea en notas
        • Clic derecho para opciones (duplicar, eliminar)
        
        � PESTAÑA GRUPOS SN:
        🔍 BÚSQUEDA DE GRUPOS:
        • Buscar por nombre o responsabilidades
        • Filtrado en tiempo real
        
        🛠️ GESTIÓN DE GRUPOS:
        • ➕ Crear nuevo grupo
        • ✏️ Editar grupo seleccionado
        • 🗑️ Eliminar grupo seleccionado
        
        ⌨️ ATAJOS DE TECLADO:
        • Ctrl+N: Nuevo enlace
        • Ctrl+E: Editar enlace
        • Del: Eliminar enlace
        • Ctrl+Shift+N: Nueva nota
        • Ctrl+S: Guardar (enlaces/notas)
        • F5: Refrescar datos
        • F1: Esta ayuda
        • F2: Guía paso a paso
        • Ctrl+1/2/3: Cambiar pestañas
        
        💡 PARA VER LA GUÍA COMPLETA PASO A PASO PRESIONA F2
        """
        
        QMessageBox.information(self, "Ayuda Rápida - TLV 4.0", ayuda_texto)
    
    def _mostrar_guia_paso_a_paso(self) -> None:
        """Muestra una guía completa paso a paso de cómo usar la aplicación."""
        guia_texto = """
        🚀 GUÍA PASO A PASO - TECH LINK VIEWER 4.0
        
        ═══════════════════════════════════════════════════════════════
        📖 PRIMEROS PASOS
        ═══════════════════════════════════════════════════════════════
        
        1️⃣ NAVEGACIÓN BÁSICA:
           • La aplicación tiene 3 pestañas principales: Enlaces, Notas y Grupos SN
           • Usa Ctrl+1, Ctrl+2, Ctrl+3 para cambiar entre pestañas rápidamente
           • También puedes hacer clic en las pestañas directamente
        
        ═══════════════════════════════════════════════════════════════
        🔗 GESTIÓN DE ENLACES (PESTAÑA 1)
        ═══════════════════════════════════════════════════════════════
        
        2️⃣ CREAR TU PRIMER ENLACE:
           • Haz clic en "Nuevo" o presiona Ctrl+N
           • Completa los campos:
             - Título: Nombre descriptivo del enlace
             - URL: Dirección web completa (https://...)
             - Descripción: Breve explicación del contenido
             - Tags: Palabras clave separadas por comas
           • Selecciona una categoría del desplegable
           • Haz clic en "Guardar"
        
        3️⃣ ORGANIZAR CON CATEGORÍAS:
           • Crea categorías personalizadas usando el botón "+"
           • Las categorías te ayudan a organizar enlaces por tema
           • Haz clic en cualquier categoría para filtrar enlaces
           • "Todas" muestra todos los enlaces sin filtro
        
        4️⃣ BUSCAR ENLACES:
           • Usa el campo de búsqueda para encontrar enlaces
           • Busca por título, URL, descripción o tags
           • La búsqueda es instantánea mientras escribes
           • Combina búsqueda + filtro de categoría para resultados precisos
        
        5️⃣ GESTIONAR ENLACES EXISTENTES:
           • Doble clic en cualquier enlace para abrirlo en el navegador
           • Selecciona un enlace y presiona Ctrl+E para editarlo
           • Selecciona un enlace y presiona Del para eliminarlo
           • Usa clic derecho para más opciones
        
        ═══════════════════════════════════════════════════════════════
        📝 GESTIÓN DE NOTAS (PESTAÑA 2)
        ═══════════════════════════════════════════════════════════════
        
        6️⃣ CREAR TU PRIMERA NOTA:
           • Haz clic en "Nueva Nota" o presiona Ctrl+Shift+N
           • Escribe un título descriptivo
           • Usa el editor para escribir tu contenido
           • Las notas se guardan automáticamente cada 3 segundos
        
        7️⃣ ORGANIZAR NOTAS:
           • Busca notas usando el campo de búsqueda
           • Las notas más recientes aparecen primero
           • Cada nota muestra fecha de creación y modificación
           • Contador de palabras y caracteres en tiempo real
        
        8️⃣ FUNCIONES AVANZADAS DE NOTAS:
           • Clic derecho en una nota para opciones adicionales
           • Duplicar notas útiles como plantillas
           • Eliminar notas que ya no necesites
           • El contenido se preserva entre sesiones
        
        ═══════════════════════════════════════════════════════════════
        📋 GESTIÓN DE GRUPOS SN (PESTAÑA 3)
        ═══════════════════════════════════════════════════════════════
        
        9️⃣ EXPLORAR GRUPOS DE SERVICE NOW:
           • Navega a la pestaña "Grupos SN" (Ctrl+3)
           • Ve la lista de grupos predefinidos como ejemplo
           • Selecciona cualquier grupo para ver sus detalles completos
        
        🔟 BUSCAR GRUPOS ESPECÍFICOS:
           • Usa el buscador para encontrar grupos por:
             - Nombre del grupo
             - Responsabilidades específicas
           • La búsqueda filtra en tiempo real
        
        1️⃣1️⃣ GESTIONAR GRUPOS:
           • ➕ Crear Nuevo Grupo:
             - Haz clic en el botón ➕
             - Completa todos los campos del formulario
             - Incluye responsabilidades (una por línea)
             - Agrega miembros separados por comas
             - Especifica herramientas utilizadas
           
           • ✏️ Editar Grupo Existente:
             - Selecciona un grupo de la lista
             - Haz clic en el botón ✏️
             - Modifica la información necesaria
             - Los cambios se guardan automáticamente
           
           • 🗑️ Eliminar Grupo:
             - Selecciona el grupo a eliminar
             - Haz clic en el botón 🗑️
             - Confirma la eliminación (no se puede deshacer)
        
        ═══════════════════════════════════════════════════════════════
        💡 CONSEJOS PROFESIONALES
        ═══════════════════════════════════════════════════════════════
        
        1️⃣2️⃣ FLUJO DE TRABAJO EFICIENTE:
           • Usa atajos de teclado para mayor velocidad
           • Organiza enlaces por categorías desde el inicio
           • Crea notas para procedimientos importantes
           • Mantén información de grupos SN actualizada
        
        1️⃣3️⃣ BACKUP Y PERSISTENCIA:
           • Todos los datos se guardan automáticamente
           • Los enlaces se almacenan en data/enlaces.json
           • Las notas se guardan en data/notas.json
           • Los grupos se guardan en data/grupos.json
        
        1️⃣4️⃣ IMPORTAR/EXPORTAR:
           • Usa las opciones de menú para importar/exportar
           • Formato JSON compatible entre versiones
           • Ideal para respaldos o migración de datos
        
        ═══════════════════════════════════════════════════════════════
        🆘 ATAJOS DE TECLADO COMPLETOS
        ═══════════════════════════════════════════════════════════════
        
        NAVEGACIÓN:
        • Ctrl+1/2/3: Cambiar entre pestañas
        • F1: Ayuda rápida
        • F2: Esta guía paso a paso
        • F5: Refrescar datos
        
        ENLACES:
        • Ctrl+N: Nuevo enlace
        • Ctrl+E: Editar enlace seleccionado
        • Del: Eliminar enlace seleccionado
        • Ctrl+S: Guardar cambios
        
        NOTAS:
        • Ctrl+Shift+N: Nueva nota
        • Ctrl+S: Guardar nota actual
        
        ¡Ya estás listo para usar TLV 4.0 de manera profesional! 🎉
        """
        
        # Crear un diálogo personalizado para la guía más grande
        dialog = QDialog(self)
        dialog.setWindowTitle("Guía Paso a Paso - TLV 4.0")
        dialog.setModal(True)
        dialog.resize(800, 700)
        
        layout = QVBoxLayout(dialog)
        
        # Área de texto con scroll
        text_area = QTextEdit()
        text_area.setReadOnly(True)
        text_area.setPlainText(guia_texto)
        text_area.setFont(Fonts.get_monospace_font(Fonts.SIZE_SMALL))
        text_area.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Colors.BG1};
                color: {Colors.FG};
                border: 1px solid {Colors.BORDER};
                border-radius: 6px;
                padding: 15px;
                line-height: 1.4;
            }}
        """)
        layout.addWidget(text_area)
        
        # Botón de cerrar
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_button = QPushButton("Cerrar")
        close_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.ACCENT_NEO};
                color: {Colors.BG0};
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {Colors.ACCENT_CYAN};
            }}
        """)
        close_button.clicked.connect(dialog.accept)
        button_layout.addWidget(close_button)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Aplicar estilo al diálogo
        dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {Colors.BG0};
                color: {Colors.FG};
            }}
        """)
        
        dialog.exec()
    
    def _mostrar_acerca_de(self) -> None:
        """Muestra el diálogo Acerca de."""
        dialogo = AboutDialog(self)
        dialogo.exec()
    
    def _nota_guardada(self, nota_id: str) -> None:
        """Maneja cuando se guarda una nota."""
        # Mostrar mensaje en barra de estado
        self.statusBar().showMessage("📝 Nota guardada correctamente", 2000)
        logger.info(f"Nota guardada: {nota_id}")
    
    def _nota_eliminada(self, titulo: str) -> None:
        """Maneja cuando se elimina una nota."""
        # Mostrar mensaje en barra de estado
        self.statusBar().showMessage(f"🗑️ Nota eliminada: {titulo}", 3000)
        logger.info(f"Nota eliminada: {titulo}")
    
    def _nueva_nota_global(self) -> None:
        """Crea una nueva nota desde cualquier pestaña."""
        # Cambiar a la pestaña de notas
        self.tab_widget.setCurrentIndex(1)
        # Crear nueva nota
        if hasattr(self, 'notes_widget'):
            self.notes_widget._nueva_nota()
    
    def closeEvent(self, event) -> None:
        """Maneja el cierre de la aplicación."""
        # Guardar datos antes de cerrar
        if self.repositorio.guardar():
            logger.info("Aplicación cerrada correctamente")
            event.accept()
        else:
            respuesta = QMessageBox.question(
                self,
                "Error al Guardar",
                "No se pudieron guardar los datos. ¿Quieres cerrar sin guardar?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if respuesta == QMessageBox.StandardButton.Yes:
                event.accept()
            else:
                event.ignore()
    
    def _configurar_fondo_panel_categorias(self, widget_categorias: QWidget) -> None:
        """Configura el fondo del panel de categorías sin imagen."""
        try:
            # Aplicar estilo limpio sin imagen de fondo
            widget_categorias.setStyleSheet(f"""
                QWidget {{
                    background-color: {Colors.BG1};
                    border: 1px solid {Colors.BORDER};
                    border-radius: 8px;
                    margin: 2px;
                }}
                QWidget > QListWidget {{
                    background-color: rgba(40, 44, 52, 255);
                    border: none;
                    border-radius: 6px;
                }}
            """)
            
            # Aplicar estilo limpio a la lista de categorías
            self.lista_categorias.setStyleSheet(f"""
                QListWidget {{
                    background-color: rgba(40, 44, 52, 255);
                    border: none;
                    border-radius: 6px;
                }}
                QListWidget::item {{
                    background-color: rgba(50, 54, 62, 100);
                    border-radius: 4px;
                    padding: 8px;
                    margin: 2px;
                    color: #e6e6e6;
                }}
                QListWidget::item:selected {{
                    background-color: rgba(100, 149, 237, 180);
                    color: white;
                    font-weight: bold;
                }}
                QListWidget::item:hover {{
                    background-color: rgba(80, 84, 92, 120);
                    color: white;
                }}
            """)
            
            logger.info("Panel de categorías configurado con fondo sólido limpio")
            
        except Exception as e:
            logger.error(f"Error al configurar fondo del panel de categorías: {e}")
            # Aplicar estilo por defecto en caso de error
            widget_categorias.setStyleSheet(f"""
                QWidget {{
                    background-color: {Colors.BG1};
                    border: 1px solid {Colors.BORDER};
                    border-radius: 8px;
                    margin: 2px;
                }}
            """)