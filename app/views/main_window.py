"""
Ventana principal de la aplicación.
"""
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLineEdit, QPushButton, QListWidget, QTableView,
    QSplitter, QLabel, QMessageBox, QFileDialog,
    QStatusBar, QMenuBar, QMenu, QFrame, QApplication,
    QToolBar, QToolButton
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QUrl
from PyQt6.QtGui import QKeySequence, QShortcut, QFont, QAction, QDesktopServices
from ..models.repository import RepositorioEnlaces
from ..models.link_model import ModeloTablaEnlaces
from ..models.search import (
    buscar_enlaces, extraer_todas_las_categorias, 
    extraer_todos_los_tags
)
from ..utils.io import abrir_url
from ..theme import Colors, Fonts, get_icon
from ..widgets import TitleBar
from ..widgets.about_dialog import AboutDialog
from ..delegates import TagDelegate
from .link_dialog import DialogoEnlace


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
        self.setCentralWidget(central_widget)
        
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
        self.boton_ayuda.setToolTip("Ayuda y documentación (F1)")
        toolbar.addWidget(self.boton_ayuda)
        
        # Botón Acerca de
        self.boton_acerca_de = QToolButton()
        self.boton_acerca_de.setIcon(get_icon('info'))
        self.boton_acerca_de.setText("Acerca de")
        self.boton_acerca_de.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.boton_acerca_de.setToolTip("Acerca de TLV 4.0 y desarrollador")
        toolbar.addWidget(self.boton_acerca_de)
        
        self.addToolBar(toolbar)
    
    def _crear_area_principal(self, layout_padre: QVBoxLayout) -> None:
        """Crea el área principal con el splitter."""
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Panel izquierdo - Categorías
        self._crear_panel_categorias(splitter)
        
        # Panel derecho - Tabla de enlaces
        self._crear_panel_enlaces(splitter)
        
        # Configurar proporciones del splitter
        splitter.setSizes([250, 750])
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)
        
        layout_padre.addWidget(splitter)
    
    def _crear_panel_categorias(self, splitter: QSplitter) -> None:
        """Crea el panel de categorías con estilo terminal."""
        widget_categorias = QWidget()
        layout_categorias = QVBoxLayout(widget_categorias)
        
        # Título
        label_categorias = QLabel("CATEGORÍAS")
        label_categorias.setFont(Fonts.get_monospace_font(Fonts.SIZE_MEDIUM, bold=True))
        label_categorias.setStyleSheet(f"color: {Colors.ACCENT_CYAN}; padding: 8px;")
        layout_categorias.addWidget(label_categorias)
        
        # Lista de categorías
        self.lista_categorias = QListWidget()
        self.lista_categorias.setMaximumWidth(300)
        layout_categorias.addWidget(self.lista_categorias)
        
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
        
        # Configurar altura de filas para mejor legibilidad
        self.tabla_enlaces.verticalHeader().setDefaultSectionSize(40)  # Altura de 40px por fila
        self.tabla_enlaces.verticalHeader().setMinimumSectionSize(35)  # Mínimo 35px
        
        # Aplicar delegate de tags para la columna de tags
        self.tag_delegate = TagDelegate()
        # Asumiendo que la columna de tags es la columna 3 (0-indexada)
        self.tabla_enlaces.setItemDelegateForColumn(3, self.tag_delegate)
        
        # Configurar columnas
        header = self.tabla_enlaces.horizontalHeader()
        header.setStretchLastSection(True)
        
        layout_enlaces.addWidget(self.tabla_enlaces)
        
        splitter.addWidget(widget_enlaces)
    
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
        self.boton_acerca_de.clicked.connect(self._mostrar_acerca_de)
        
        # Categorías
        self.lista_categorias.itemClicked.connect(self._categoria_seleccionada)
        
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
        self.lista_categorias.addItem(f"📂 Todas ({total_enlaces})")
        
        # Agregar categorías específicas
        categorias = extraer_todas_las_categorias(enlaces)
        for categoria in categorias:
            # Contar enlaces en esta categoría
            count = sum(1 for enlace in enlaces if enlace.get('categoria') == categoria)
            self.lista_categorias.addItem(f"📁 {categoria} ({count})")
    
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
        
        if texto.startswith("📂 Todas"):
            self.categoria_filtro_actual = ""
        else:
            # Extraer nombre de categoría del texto "📁 Nombre (count)"
            inicio = texto.find(" ") + 1
            fin = texto.rfind(" (")
            if fin > inicio:
                self.categoria_filtro_actual = texto[inicio:fin]
            else:
                self.categoria_filtro_actual = texto[inicio:]
        
        self.tag_filtro_actual = ""  # Limpiar filtro de tag
        self._actualizar_tabla_enlaces()
        self._actualizar_informacion()
    
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
        """Refresca los datos y la vista."""
        try:
            # Recargar datos del repositorio
            self.repositorio.cargar()
            
            # Actualizar todas las vistas
            self._actualizar_categorias()
            self._actualizar_tabla_enlaces()
            self._actualizar_informacion()
            
            # Mostrar mensaje en barra de estado
            self.statusBar().showMessage("Datos refrescados correctamente", 2000)
            logger.info("Datos refrescados por el usuario")
            
        except Exception as e:
            logger.error(f"Error al refrescar datos: {e}")
            QMessageBox.warning(self, "Error", f"Error al refrescar datos: {e}")
    
    def _mostrar_configuracion(self) -> None:
        """Muestra el diálogo de configuración."""
        # Por ahora, mostrar un mensaje informativo
        QMessageBox.information(
            self,
            "Configuración",
            "⚙️ Configuración de TLV 4.0\n\n"
            "🔧 Funciones disponibles:\n"
            "• Tema oscuro terminal ✓\n"
            "• Iconos SVG personalizados ✓\n"
            "• Efectos typewriter ✓\n"
            "• Atajos de teclado ✓\n\n"
            "📝 Próximamente:\n"
            "• Configuración de colores\n"
            "• Personalización de fuentes\n"
            "• Configuración de categorías\n"
            "• Configuración de exportación"
        )
    
    def _mostrar_ayuda(self) -> None:
        """Muestra la ayuda de la aplicación."""
        ayuda_texto = """
        📋 AYUDA - TECH LINK VIEWER 4.0
        
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
        
        📊 IMPORTAR/EXPORTAR:
        • Importar: Cargar enlaces desde archivo JSON
        • Exportar: Guardar enlaces a archivo JSON
        
        ⌨️ ATAJOS DE TECLADO:
        • Ctrl+N: Nuevo enlace
        • Ctrl+E: Editar enlace
        • Del: Eliminar enlace
        • F5: Refrescar datos
        • F1: Esta ayuda
        
        🎨 INTERFAZ:
        • Tema oscuro terminal profesional
        • Iconos SVG con efectos hover
        • Header con efecto typewriter animado
        """
        
        QMessageBox.information(self, "Ayuda - TLV 4.0", ayuda_texto)
    
    def _mostrar_acerca_de(self) -> None:
        """Muestra el diálogo Acerca de."""
        dialogo = AboutDialog(self)
        dialogo.exec()
    
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