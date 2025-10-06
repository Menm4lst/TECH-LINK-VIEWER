"""
Configuración global para la aplicación TECH LINK VIEWER.
"""

# Configuración de la tabla de enlaces
TABLA_CONFIG = {
    # URLs
    'url_max_chars': 60,  # Máximo de caracteres para URLs en la tabla
    'url_tooltip_extra_info': True,  # Mostrar información extra en tooltips
    
    # Filas
    'fila_altura_default': 32,  # Altura por defecto de filas
    'fila_altura_minima': 28,   # Altura mínima
    'fila_altura_maxima': 45,   # Altura máxima
    
    # Columnas (anchos)
    'columna_titulo': 250,
    'columna_url': 300,
    'columna_categoria': 120,
    'columna_tags': 200,
    
    # Comportamiento
    'word_wrap': False,  # Evitar wrap de texto que aumenta altura
    'resize_to_contents': True,  # Redimensionar columnas automáticamente
}

# Configuración de notas
NOTAS_CONFIG = {
    'archivo_notas': 'data/notas.json',
    'backup_automatico': True,
    'editor_font_size': 10,
    'editor_font_family': 'Consolas',
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