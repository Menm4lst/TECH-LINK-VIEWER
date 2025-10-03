"""
Estilos y temas para la aplicación TECH LINK VIEWER.
"""

# Tema oscuro profesional para la aplicación
TEMA_OSCURO = """
QMainWindow {
    background-color: #1e1e1e;
    color: #ffffff;
}

QWidget {
    background-color: #1e1e1e;
    color: #ffffff;
    font-family: 'Segoe UI', Arial, sans-serif;
}

/* Barra de búsqueda */
QLineEdit {
    background-color: #2d2d2d;
    border: 2px solid #404040;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 14px;
    color: #ffffff;
}

QLineEdit:focus {
    border-color: #0078d4;
    background-color: #333333;
}

QLineEdit::placeholder {
    color: #888888;
}

/* Botones */
QPushButton {
    background-color: #0078d4;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-size: 13px;
    font-weight: 600;
    min-height: 20px;
}

QPushButton:hover {
    background-color: #106ebe;
}

QPushButton:pressed {
    background-color: #005a9e;
}

QPushButton:disabled {
    background-color: #404040;
    color: #888888;
}

/* Botones secundarios */
QPushButton.secondary {
    background-color: #404040;
    color: #ffffff;
}

QPushButton.secondary:hover {
    background-color: #4a4a4a;
}

/* Botón de peligro (eliminar) */
QPushButton.danger {
    background-color: #c42b1c;
}

QPushButton.danger:hover {
    background-color: #a23a2e;
}

/* Lista de categorías */
QListWidget {
    background-color: #252526;
    border: 1px solid #404040;
    border-radius: 6px;
    outline: none;
    padding: 5px;
}

QListWidget::item {
    padding: 10px 15px;
    border: none;
    border-radius: 4px;
    margin: 2px 0px;
}

QListWidget::item:selected {
    background-color: #0078d4;
    color: white;
}

QListWidget::item:hover {
    background-color: #333333;
}

/* Tabla de enlaces */
QTableView {
    background-color: #252526;
    gridline-color: #404040;
    border: 1px solid #404040;
    border-radius: 6px;
    selection-background-color: #0078d4;
    alternate-background-color: #2a2a2a;
}

QTableView::item {
    padding: 8px;
    border: none;
}

QTableView::item:selected {
    background-color: #0078d4;
    color: white;
}

QTableView::item:hover {
    background-color: #333333;
}

QHeaderView::section {
    background-color: #323233;
    color: #ffffff;
    padding: 12px 8px;
    border: none;
    border-right: 1px solid #404040;
    font-weight: 600;
}

QHeaderView::section:hover {
    background-color: #3c3c3c;
}

/* Barras de desplazamiento */
QScrollBar:vertical {
    background-color: #2d2d2d;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #555555;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #666666;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #2d2d2d;
    height: 12px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal {
    background-color: #555555;
    border-radius: 6px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #666666;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Barra de estado */
QStatusBar {
    background-color: #323233;
    color: #ffffff;
    border-top: 1px solid #404040;
    font-size: 12px;
}

/* Menú contextual */
QMenu {
    background-color: #2d2d2d;
    border: 1px solid #404040;
    border-radius: 4px;
    padding: 4px;
}

QMenu::item {
    padding: 8px 16px;
    border-radius: 3px;
}

QMenu::item:selected {
    background-color: #0078d4;
}

/* Diálogos */
QDialog {
    background-color: #1e1e1e;
    color: #ffffff;
}

QFormLayout QLabel {
    color: #ffffff;
    font-weight: 500;
}

/* ComboBox */
QComboBox {
    background-color: #2d2d2d;
    border: 2px solid #404040;
    border-radius: 6px;
    padding: 6px 12px;
    color: #ffffff;
    min-width: 120px;
}

QComboBox:focus {
    border-color: #0078d4;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #ffffff;
    margin-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #2d2d2d;
    border: 1px solid #404040;
    border-radius: 4px;
    selection-background-color: #0078d4;
    color: #ffffff;
}

/* TextEdit para tags */
QTextEdit {
    background-color: #2d2d2d;
    border: 2px solid #404040;
    border-radius: 6px;
    padding: 8px;
    color: #ffffff;
}

QTextEdit:focus {
    border-color: #0078d4;
}

/* Tooltip */
QToolTip {
    background-color: #323233;
    color: #ffffff;
    border: 1px solid #404040;
    border-radius: 4px;
    padding: 6px;
    font-size: 12px;
}

/* Splitter */
QSplitter::handle {
    background-color: #404040;
    width: 1px;
    height: 1px;
}

QSplitter::handle:hover {
    background-color: #0078d4;
}

/* Título de la aplicación */
.app-title {
    color: #0078d4;
    font-size: 18px;
    font-weight: 700;
    font-family: 'Segoe UI', Arial, sans-serif;
    letter-spacing: 1px;
}

.app-subtitle {
    color: #888888;
    font-size: 11px;
    font-weight: 400;
    font-style: italic;
}

/* Indicadores de estado */
.status-success {
    color: #4caf50;
    font-weight: 600;
}

.status-warning {
    color: #ff9800;
    font-weight: 600;
}

.status-error {
    color: #f44336;
    font-weight: 600;
}

/* Etiquetas de categoría */
.category-badge {
    background-color: #0078d4;
    color: white;
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
}

/* Etiquetas de tags */
.tag-badge {
    background-color: #404040;
    color: #ffffff;
    padding: 3px 6px;
    border-radius: 8px;
    font-size: 10px;
    margin: 2px;
}

/* Efectos de brillo para elementos interactivos */
.glow-blue {
    box-shadow: 0 0 10px rgba(0, 120, 212, 0.5);
}

.glow-green {
    box-shadow: 0 0 10px rgba(76, 175, 80, 0.5);
}
"""

def aplicar_tema_oscuro(app):
    """
    Aplica el tema oscuro a la aplicación.
    
    Args:
        app: Instancia de QApplication
    """
    app.setStyleSheet(TEMA_OSCURO)

def obtener_icono_app():
    """
    Retorna el código para crear un icono de la aplicación usando caracteres.
    """
    return "🔗"  # Icono de enlace

def obtener_titulo_app():
    """
    Retorna el título completo de la aplicación.
    """
    return "TECH LINK VIEWER"

def obtener_subtitulo_app():
    """
    Retorna el subtítulo de la aplicación.
    """
    return "Buscador Global de Enlaces v4.0"

def obtener_version_app():
    """
    Retorna la versión de la aplicación.
    """
    return "4.0.1"