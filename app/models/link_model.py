"""
Modelo de tabla para mostrar enlaces en PyQt6.
"""
from typing import List, Dict, Any, Optional, Tuple
from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from ..utils.time import formatear_fecha


class ModeloTablaEnlaces(QAbstractTableModel):
    """
    Modelo personalizado para mostrar enlaces en QTableView.
    """
    
    # Señales personalizadas
    enlace_doble_click = pyqtSignal(str)  # Emite ID del enlace
    tag_clickeado = pyqtSignal(str)       # Emite tag clickeado
    
    def __init__(self):
        super().__init__()
        self._enlaces: List[Dict[str, Any]] = []
        self._enlaces_con_score: List[Tuple[Dict[str, Any], float]] = []
        self._columnas = ["Título", "URL", "Categoría", "Tags", "Actualizado"]
        self._usar_scores = False
    
    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Retorna el número de filas."""
        return len(self._enlaces)
    
    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Retorna el número de columnas."""
        return len(self._columnas)
    
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        """
        Retorna los datos para mostrar en la tabla.
        
        Args:
            index: Índice de la celda
            role: Rol de los datos (display, font, color, etc.)
            
        Returns:
            Datos a mostrar
        """
        if not index.isValid() or not (0 <= index.row() < len(self._enlaces)):
            return QVariant()
        
        enlace = self._enlaces[index.row()]
        columna = index.column()
        
        if role == Qt.ItemDataRole.DisplayRole:
            return self._obtener_dato_display(enlace, columna)
        elif role == Qt.ItemDataRole.FontRole:
            return self._obtener_fuente(enlace, columna)
        elif role == Qt.ItemDataRole.ForegroundRole:
            return self._obtener_color_texto(enlace, columna)
        elif role == Qt.ItemDataRole.ToolTipRole:
            return self._obtener_tooltip(enlace, columna)
        elif role == Qt.ItemDataRole.UserRole:
            # Rol personalizado para obtener el ID del enlace
            return enlace.get('id', '')
        
        return QVariant()
    
    def _obtener_dato_display(self, enlace: Dict[str, Any], columna: int) -> str:
        """Obtiene el dato a mostrar para una columna específica."""
        if columna == 0:  # Título
            titulo = enlace.get('titulo', '')
            # Si hay score, mostrar indicador de relevancia
            if self._usar_scores:
                score = self._obtener_score_enlace(enlace)
                if score < 0.5:
                    return f"🔍 {titulo}"  # Indicador de búsqueda fuzzy
            return titulo
            
        elif columna == 1:  # URL
            url = enlace.get('url', '')
            # Truncar URL si es muy larga
            if len(url) > 50:
                return url[:47] + "..."
            return url
            
        elif columna == 2:  # Categoría
            return enlace.get('categoria', '')
            
        elif columna == 3:  # Tags
            tags = enlace.get('tags', [])
            if isinstance(tags, list):
                return ", ".join(tags)
            return ""
            
        elif columna == 4:  # Fecha actualización
            timestamp = enlace.get('actualizado_en', '')
            return formatear_fecha(timestamp)
        
        return ""
    
    def _obtener_fuente(self, enlace: Dict[str, Any], columna: int) -> Optional[QFont]:
        """Obtiene la fuente para una celda específica."""
        fuente = QFont()
        
        if columna == 0:  # Título en negrita
            fuente.setBold(True)
        elif columna == 3:  # Tags en cursiva
            fuente.setItalic(True)
            fuente.setPointSize(9)
        
        return fuente
    
    def _obtener_color_texto(self, enlace: Dict[str, Any], columna: int) -> Optional[QColor]:
        """Obtiene el color del texto para una celda específica."""
        if columna == 1:  # URL en azul
            return QColor(0, 0, 255)
        elif columna == 3:  # Tags en gris
            return QColor(100, 100, 100)
        elif columna == 4:  # Fecha en gris claro
            return QColor(150, 150, 150)
        
        return None
    
    def _obtener_tooltip(self, enlace: Dict[str, Any], columna: int) -> str:
        """Obtiene el tooltip para una celda específica."""
        if columna == 0:  # Título
            return f"Título: {enlace.get('titulo', '')}\nDoble clic para abrir"
        elif columna == 1:  # URL completa
            return f"URL: {enlace.get('url', '')}\nDoble clic para abrir"
        elif columna == 2:  # Categoría
            return f"Categoría: {enlace.get('categoria', '')}\nClic para filtrar"
        elif columna == 3:  # Tags
            tags = enlace.get('tags', [])
            if tags:
                return f"Tags: {', '.join(tags)}\nClic en un tag para filtrar"
            return "Sin tags"
        elif columna == 4:  # Información de fechas
            creado = enlace.get('creado_en', '')
            actualizado = enlace.get('actualizado_en', '')
            return f"Creado: {formatear_fecha(creado)}\nActualizado: {formatear_fecha(actualizado)}"
        
        return ""
    
    def _obtener_score_enlace(self, enlace: Dict[str, Any]) -> float:
        """Obtiene el score de un enlace si está disponible."""
        enlace_id = enlace.get('id', '')
        for enlace_score, score in self._enlaces_con_score:
            if enlace_score.get('id') == enlace_id:
                return score
        return 1.0
    
    def headerData(self, section: int, orientation: Qt.Orientation, 
                  role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        """
        Retorna los datos de los encabezados.
        
        Args:
            section: Número de sección (columna o fila)
            orientation: Orientación (horizontal o vertical)
            role: Rol de los datos
            
        Returns:
            Datos del encabezado
        """
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                if 0 <= section < len(self._columnas):
                    return self._columnas[section]
            else:
                return str(section + 1)
        elif role == Qt.ItemDataRole.FontRole and orientation == Qt.Orientation.Horizontal:
            fuente = QFont()
            fuente.setBold(True)
            return fuente
        
        return QVariant()
    
    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        """Retorna las flags para una celda específica."""
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
    
    def actualizar_enlaces(self, enlaces: List[Dict[str, Any]]) -> None:
        """
        Actualiza la lista de enlaces mostrados.
        
        Args:
            enlaces: Nueva lista de enlaces
        """
        self.beginResetModel()
        self._enlaces = enlaces.copy()
        self._enlaces_con_score = []
        self._usar_scores = False
        self.endResetModel()
    
    def actualizar_enlaces_con_score(self, enlaces_con_score: List[Tuple[Dict[str, Any], float]]) -> None:
        """
        Actualiza la lista de enlaces con scores de búsqueda.
        
        Args:
            enlaces_con_score: Lista de tuplas (enlace, score)
        """
        self.beginResetModel()
        self._enlaces = [enlace for enlace, _ in enlaces_con_score]
        self._enlaces_con_score = enlaces_con_score.copy()
        self._usar_scores = True
        self.endResetModel()
    
    def obtener_enlace_por_fila(self, fila: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene el enlace de una fila específica.
        
        Args:
            fila: Número de fila
            
        Returns:
            Diccionario con el enlace o None si la fila no es válida
        """
        if 0 <= fila < len(self._enlaces):
            return self._enlaces[fila]
        return None
    
    def obtener_id_enlace_por_fila(self, fila: int) -> Optional[str]:
        """
        Obtiene el ID del enlace de una fila específica.
        
        Args:
            fila: Número de fila
            
        Returns:
            ID del enlace o None si la fila no es válida
        """
        enlace = self.obtener_enlace_por_fila(fila)
        return enlace.get('id') if enlace else None
    
    def obtener_tag_en_posicion(self, fila: int, columna: int, posicion_x: int) -> Optional[str]:
        """
        Obtiene el tag específico en una posición de clic dentro de la celda de tags.
        
        Args:
            fila: Número de fila
            columna: Número de columna
            posicion_x: Posición X del clic dentro de la celda
            
        Returns:
            Tag clickeado o None si no se clickeó en un tag
        """
        if columna != 3:  # Solo la columna de tags
            return None
        
        enlace = self.obtener_enlace_por_fila(fila)
        if not enlace:
            return None
        
        tags = enlace.get('tags', [])
        if not tags:
            return None
        
        # Aproximación simple: dividir el ancho de la celda entre los tags
        # En una implementación más avanzada, se calcularía el ancho real de cada tag
        texto_tags = ", ".join(tags)
        if posicion_x > 0 and len(texto_tags) > 0:
            # Calcular qué tag fue clickeado basado en la posición aproximada
            posicion_relativa = posicion_x / 200  # Ancho aproximado de celda
            indice_tag = int(posicion_relativa * len(tags))
            
            if 0 <= indice_tag < len(tags):
                return tags[indice_tag]
        
        return None
    
    def limpiar(self) -> None:
        """Limpia todos los datos del modelo."""
        self.beginResetModel()
        self._enlaces = []
        self._enlaces_con_score = []
        self._usar_scores = False
        self.endResetModel()
    
    def esta_vacio(self) -> bool:
        """Retorna True si el modelo no tiene datos."""
        return len(self._enlaces) == 0
    
    def obtener_numero_enlaces(self) -> int:
        """Retorna el número total de enlaces."""
        return len(self._enlaces)