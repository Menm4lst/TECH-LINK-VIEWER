"""
Configuración global para la aplicación TECH LINK VIEWER.
"""

# Configuración de la tabla de enlaces
TABLA_CONFIG = {
    # URLs
    'url_max_chars': 60,  # Máximo de caracteres para URLs en la tabla
    'url_tooltip_extra_info': True,  # Mostrar información extra en tooltips
    
    # Filas
    'fila_altura_default': 36,  # Altura por defecto de filas (aumentada para mejor legibilidad)
    'fila_altura_minima': 32,   # Altura mínima
    'fila_altura_maxima': 48,   # Altura máxima
    
    # Columnas (anchos optimizados)
    'columna_titulo': 280,
    'columna_url': 320,
    'columna_categoria': 140,
    'columna_tags': 220,
    
    # Colores de selección
    'color_seleccion': '#8A2BE2',  # Violeta para elementos seleccionados
    'color_seleccion_texto': '#FFFFFF',  # Texto blanco sobre violeta
    'color_hover': '#9932CC',  # Violeta más claro para hover
    'color_fila_alternada': '#2a2a2a',  # Filas alternas más suaves
    'color_borde_tabla': '#404040',  # Bordes de tabla más suaves
    
    # Comportamiento
    'word_wrap': False,  # Evitar wrap de texto que aumenta altura
    'resize_to_contents': True,  # Redimensionar columnas automáticamente
}

# Configuración de notas
NOTAS_CONFIG = {
    'archivo_notas': 'data/notas.json',
    'backup_automatico': True,
    'editor_font_size': 11,  # Aumentado para mejor legibilidad
    'editor_font_family': 'Consolas',
    'editor_line_height': 1.4,  # Espaciado entre líneas mejorado
}

# Sistema de colores unificado (Material Design 3 adaptado)
COLOR_SCHEME = {
    # Colores primarios
    'primary': '#8A2BE2',           # Violeta principal
    'primary_variant': '#9932CC',    # Violeta claro
    'primary_dark': '#6A1B9A',      # Violeta oscuro
    
    # Colores de superficie
    'surface': '#1e1e1e',           # Fondo principal
    'surface_variant': '#2a2a2a',   # Fondo alternativo
    'surface_elevated': '#2f2f2f',  # Elementos elevados
    
    # Colores de texto
    'on_surface': '#ffffff',        # Texto sobre superficie
    'on_surface_variant': '#e0e0e0', # Texto secundario
    'on_primary': '#ffffff',        # Texto sobre primario
    
    # Colores de estado
    'success': '#4CAF50',           # Verde para éxito
    'warning': '#FF9800',           # Naranja para advertencia
    'error': '#F44336',             # Rojo para error
    'info': '#2196F3',              # Azul para información
    
    # Bordes y divisores
    'outline': '#404040',           # Bordes sutiles
    'outline_variant': '#303030',   # Bordes más suaves
}

# Configuración de tipografía
TYPOGRAPHY = {
    'font_family_primary': 'Segoe UI',
    'font_family_monospace': 'Consolas',
    'font_sizes': {
        'display': 24,      # Títulos grandes
        'headline': 18,     # Títulos sección
        'title': 16,        # Títulos pequeños
        'body': 14,         # Texto principal
        'caption': 12,      # Texto pequeño
        'overline': 10      # Texto muy pequeño
    },
    'font_weights': {
        'regular': 400,
        'medium': 500,
        'semibold': 600,
        'bold': 700
    }
}

# Configuración de espaciado (basado en Material Design)
SPACING = {
    'xs': 4,    # 4px
    'sm': 8,    # 8px
    'md': 16,   # 16px
    'lg': 24,   # 24px
    'xl': 32,   # 32px
    'xxl': 48   # 48px
}

# Configuración de bordes y sombras
ELEVATION = {
    'border_radius': {
        'small': 4,
        'medium': 8,
        'large': 12,
        'xlarge': 16
    },
    'shadows': {
        'none': 'none',
        'small': '0 1px 3px rgba(0,0,0,0.3)',
        'medium': '0 2px 6px rgba(0,0,0,0.4)',
        'large': '0 4px 12px rgba(0,0,0,0.5)'
    }
}

# Configuración general
APP_CONFIG = {
    'version': '4.0',
    'titulo': 'TECH LINK VIEWER',
    'subtitulo': 'Global Link Search',
    'desarrollador': 'ANTWARE',
    'ventana_minima_ancho': 1000,
    'ventana_minima_altura': 700,
    'ventana_default_ancho': 1200,
    'ventana_default_altura': 800,
}

def obtener_config_tabla():
    """Obtiene la configuración de la tabla."""
    return TABLA_CONFIG.copy()

def obtener_config_notas():
    """Obtiene la configuración de notas."""
    return NOTAS_CONFIG.copy()

def obtener_config_app():
    """Obtiene la configuración general."""
    return APP_CONFIG.copy()

def actualizar_config_tabla(**kwargs):
    """Actualiza la configuración de la tabla."""
    TABLA_CONFIG.update(kwargs)

def actualizar_config_notas(**kwargs):
    """Actualiza la configuración de notas."""
    NOTAS_CONFIG.update(kwargs)

# Nuevas funciones para el sistema de diseño mejorado
def obtener_color_scheme():
    """Obtiene el esquema de colores unificado"""
    return COLOR_SCHEME.copy()

def obtener_typography():
    """Obtiene la configuración de tipografía"""
    return TYPOGRAPHY.copy()

def obtener_spacing():
    """Obtiene la configuración de espaciado"""
    return SPACING.copy()

def obtener_elevation():
    """Obtiene la configuración de elevación y sombras"""
    return ELEVATION.copy()

def get_color(color_name: str) -> str:
    """Obtiene un color específico del esquema de colores"""
    return COLOR_SCHEME.get(color_name, '#ffffff')

def get_font_size(size_name: str) -> int:
    """Obtiene un tamaño de fuente específico"""
    return TYPOGRAPHY['font_sizes'].get(size_name, 14)

def get_spacing(size_name: str) -> int:
    """Obtiene un espaciado específico"""
    return SPACING.get(size_name, 16)

def get_border_radius(size_name: str) -> int:
    """Obtiene un radio de borde específico"""
    return ELEVATION['border_radius'].get(size_name, 8)

def get_shadow(level: str) -> str:
    """Obtiene una sombra específica"""
    return ELEVATION['shadows'].get(level, 'none')