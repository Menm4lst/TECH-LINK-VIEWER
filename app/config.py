"""
Configuración global para la aplicación TECH LINK VIEWER 4.0
Sistema de configuración con tema oscuro violeta y tipografía aumentada
"""

# Configuración de la aplicación
APP_CONFIG = {
    'nombre': 'TECH LINK VIEWER',
    'version': '4.0',
    'autor': 'DevTeam',
    'descripcion': 'Visor avanzado de enlaces técnicos con funcionalidades modernas',
    
    # Configuración de la ventana
    'ventana_ancho': 1400,
    'ventana_alto': 900,
    'ventana_redimensionable': True,
    'ventana_centrada': True,
    
    # Configuración del tema
    'tema_predeterminado': 'fluent_dark_violet',
    'tema_personalizable': True,
}

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
    'color_seleccion': '#9D4EDD',  # Violeta para elementos seleccionados
    'color_seleccion_texto': '#FFFFFF',  # Texto blanco sobre violeta
    'color_hover': '#C77DFF',  # Violeta más claro para hover
    'color_fila_alternada': '#2D1B42',  # Filas alternas violeta oscuro
    'color_borde_tabla': '#4B2B70',  # Bordes de tabla violeta
    
    # Comportamiento
    'word_wrap': False,  # Evitar wrap de texto que aumenta altura
    'resize_to_contents': True,  # Redimensionar columnas automáticamente
}

# Configuración de notas - Tipografía aumentada para mejor legibilidad
NOTAS_CONFIG = {
    'archivo_notas': 'data/notas.json',
    'backup_automatico': True,
    'editor_font_size': 16,  # Aumentado significativamente para mejor legibilidad
    'editor_font_family': 'Consolas',
    'editor_line_height': 1.6,  # Espaciado entre líneas mejorado para lectura
}

# Esquema de colores Fluent Design System - Tema Oscuro Violeta
FLUENT_COLOR_SCHEME = {
    # Colores primarios violetas
    'primary': '#9D4EDD',           # Violeta principal
    'primary_light': '#C77DFF',     # Violeta claro para hover
    'primary_dark': '#7209B7',      # Violeta oscuro para pressed
    'primary_variant': '#E0AAFF',   # Variante violeta suave
    'accent': '#9D4EDD',            # Acento violeta
    
    # Superficies oscuras con tonos violetas
    'surface_primary': '#1A1625',   # Superficie principal oscura
    'surface_secondary': '#2D1B42', # Superficie secundaria violeta oscuro
    'surface_tertiary': '#3C2359',  # Superficie terciaria violeta medio
    'surface_variant': '#4B2B70',   # Superficie variante violeta
    'surface_elevated': '#2D1B42',  # Superficie elevada violeta oscuro
    'surface_dark': '#0F0B16',      # Superficie muy oscura
    'surface_dark_alt': '#1A1625',  # Superficie oscura alternativa
    
    # Materiales acrílicos oscuros con tonos violetas
    'acrylic_light': 'rgba(45, 27, 66, 0.85)',        # Acrílico violeta claro
    'acrylic_medium': 'rgba(60, 35, 89, 0.9)',        # Acrílico violeta medio
    'acrylic_dark': 'rgba(26, 22, 37, 0.95)',         # Acrílico muy oscuro
    'acrylic_accent': 'rgba(157, 78, 221, 0.15)',     # Acrílico con acento violeta
    
    # Colores de texto para tema oscuro
    'text_primary': '#E8E3F3',      # Texto principal claro
    'text_secondary': '#B8A9C9',    # Texto secundario violeta suave
    'text_tertiary': '#8B7D9B',     # Texto terciario violeta medio
    'text_disabled': '#5A4D6B',     # Texto deshabilitado
    'text_on_accent': '#FFFFFF',    # Texto sobre acento (blanco)
    'text_hyperlink': '#C77DFF',    # Enlaces violeta claro
    
    # Compatibilidad con sistema anterior
    'on_surface': '#E8E3F3',        # Equivalente a text_primary
    'on_primary': '#FFFFFF',        # Equivalente a text_on_accent
    'on_surface_variant': '#B8A9C9', # Equivalente a text_secondary
    
    # Colores de estado para tema oscuro
    'success': '#4CAF50',           # Verde éxito
    'warning': '#FF9800',           # Naranja advertencia
    'error': '#F44336',             # Rojo error
    'info': '#9D4EDD',              # Violeta información
    
    # Bordes y divisores oscuros
    'stroke_primary': '#4B2B70',    # Borde principal violeta
    'stroke_secondary': '#3C2359',  # Borde secundario violeta oscuro
    'stroke_tertiary': '#2D1B42',   # Borde terciario muy sutil
    'stroke_accent': '#9D4EDD',     # Borde acento violeta
    'stroke_focus': '#C77DFF',      # Borde focus violeta claro
    
    # Compatibilidad con sistema anterior
    'outline': '#4B2B70',           # Equivalente a stroke_primary
    'outline_variant': '#3C2359',   # Equivalente a stroke_secondary
    
    # Efectos de hover y selección violetas
    'hover_light': 'rgba(157, 78, 221, 0.08)',        # Hover sutil violeta
    'hover_medium': 'rgba(157, 78, 221, 0.15)',       # Hover medio violeta
    'selection': 'rgba(157, 78, 221, 0.25)',          # Selección violeta
    'selection_strong': '#9D4EDD',                     # Selección fuerte violeta
    
    # Reveal effects violetas
    'reveal_hover': 'rgba(199, 125, 255, 0.2)',       # Reveal violeta al hover
    'reveal_pressed': 'rgba(199, 125, 255, 0.1)',     # Reveal violeta presionado
}

# Tipografía Fluent (Segoe UI Variable) - Tamaños aumentados para mejor legibilidad
FLUENT_TYPOGRAPHY = {
    'font_family_primary': 'Segoe UI Variable',
    'font_family_fallback': 'Segoe UI, system-ui, sans-serif',
    'font_family_monospace': 'Cascadia Code, Consolas, monospace',
    
    'font_sizes': {
        'caption': 14,      # Texto pequeño (aumentado de 12)
        'body': 16,         # Texto principal (aumentado de 14)
        'body_strong': 16,  # Texto principal enfático
        'subtitle': 22,     # Subtítulos (aumentado de 20)
        'title': 32,        # Títulos (aumentado de 28)
        'title_large': 44,  # Títulos grandes (aumentado de 40)
        'display': 72       # Display (aumentado de 68)
    },
    
    'font_weights': {
        'regular': 400,
        'medium': 500,
        'semibold': 600,
        'bold': 700
    },
    
    'line_heights': {
        'caption': 18,      # Altura de línea para caption (aumentado de 16)
        'body': 24,         # Altura de línea para body (aumentado de 20)
        'subtitle': 30,     # Altura de línea para subtitle (aumentado de 28)
        'title': 40,        # Altura de línea para title (aumentado de 36)
        'title_large': 56,  # Altura de línea para title_large (aumentado de 52)
        'display': 88       # Altura de línea para display (aumentado de 80)
    },
    
    'letter_spacing': {
        'tight': '-0.5px',
        'normal': '0px',
        'wide': '0.5px'
    }
}

# Sistema de espaciado Fluent (4px grid)
FLUENT_SPACING = {
    'xxs': 2,    # Extra extra pequeño
    'xs': 4,     # Extra pequeño
    'sm': 8,     # Pequeño
    'md': 12,    # Medio
    'lg': 16,    # Grande
    'xl': 20,    # Extra grande
    'xxl': 24,   # Extra extra grande
    'xxxl': 32   # Máximo
}

# Sistema de elevación y sombras Fluent
FLUENT_ELEVATION = {
    'border_radius': {
        'small': 4,
        'medium': 6,
        'large': 8,
        'extra_large': 12
    },
    
    'shadows': {
        'depth_2': '0 1px 3px rgba(0, 0, 0, 0.3)',
        'depth_4': '0 2px 8px rgba(0, 0, 0, 0.3)',
        'depth_8': '0 4px 16px rgba(0, 0, 0, 0.4)',
        'depth_16': '0 8px 32px rgba(0, 0, 0, 0.5)',
        'depth_64': '0 32px 64px rgba(0, 0, 0, 0.6)'
    },
    
    'backdrop_filter': 'blur(40px) saturate(125%)',
}

# Sistema de animaciones Fluent
FLUENT_MOTION = {
    'duration': {
        'fast': '150ms',
        'normal': '300ms',
        'slow': '500ms'
    },
    
    'easing': {
        'standard': 'cubic-bezier(0.4, 0.0, 0.2, 1)',
        'decelerate': 'cubic-bezier(0.0, 0.0, 0.2, 1)',
        'accelerate': 'cubic-bezier(0.4, 0.0, 1, 1)',
        'sharp': 'cubic-bezier(0.4, 0.0, 0.6, 1)'
    }
}

# ============================================================================
# FUNCIONES DE ACCESO RÁPIDO
# ============================================================================

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

# Nuevas funciones para el sistema Fluent Design
def obtener_fluent_colors():
    """Obtiene el esquema de colores Fluent"""
    return FLUENT_COLOR_SCHEME.copy()

def obtener_fluent_typography():
    """Obtiene la configuración de tipografía Fluent"""
    return FLUENT_TYPOGRAPHY.copy()

def obtener_fluent_spacing():
    """Obtiene la configuración de espaciado Fluent"""
    return FLUENT_SPACING.copy()

def obtener_fluent_elevation():
    """Obtiene la configuración de elevación Fluent"""
    return FLUENT_ELEVATION.copy()

def obtener_fluent_motion():
    """Obtiene la configuración de animaciones Fluent"""
    return FLUENT_MOTION.copy()

def get_fluent_color(color_name: str) -> str:
    """Obtiene un color específico del esquema Fluent"""
    return FLUENT_COLOR_SCHEME.get(color_name, '#E8E3F3')

def get_fluent_font_size(size_name: str) -> int:
    """Obtiene un tamaño de fuente Fluent específico"""
    return FLUENT_TYPOGRAPHY['font_sizes'].get(size_name, 16)

def get_fluent_spacing(size_name: str) -> int:
    """Obtiene un espaciado Fluent específico"""
    return FLUENT_SPACING.get(size_name, 8)

def get_fluent_border_radius(size_name: str) -> int:
    """Obtiene un radio de borde Fluent específico"""
    return FLUENT_ELEVATION['border_radius'].get(size_name, 4)

def get_fluent_shadow(depth_name: str) -> str:
    """Obtiene una sombra Fluent específica"""
    return FLUENT_ELEVATION['shadows'].get(depth_name, '0 2px 8px rgba(0, 0, 0, 0.3)')

# ============================================================================
# FUNCIONES DE COMPATIBILIDAD (mantienen la API anterior)
# ============================================================================

def obtener_color_scheme():
    """Obtiene el esquema de colores (compatibilidad - ahora usa Fluent)"""
    return FLUENT_COLOR_SCHEME.copy()

def get_color(color_name: str) -> str:
    """Obtiene un color específico (compatibilidad - ahora usa Fluent)"""
    # Mapeo de colores antiguos a nuevos
    color_mapping = {
        'primary': 'primary',
        'primary_variant': 'primary_light',
        'primary_dark': 'primary_dark',
        'secondary': 'accent',
        'surface': 'surface_primary',
        'surface_elevated': 'surface_elevated',
        'surface_variant': 'surface_variant',
        'on_surface': 'text_primary',
        'on_primary': 'text_on_accent',
        'on_surface_variant': 'text_secondary',
        'outline': 'stroke_primary',
        'outline_variant': 'stroke_secondary'
    }
    
    fluent_color = color_mapping.get(color_name, color_name)
    return FLUENT_COLOR_SCHEME.get(fluent_color, '#E8E3F3')

def obtener_typography():
    """Obtiene la configuración de tipografía (compatibilidad - ahora usa Fluent)"""
    return FLUENT_TYPOGRAPHY.copy()

def get_font_size(size_name: str) -> int:
    """Obtiene un tamaño de fuente específico (compatibilidad - ahora usa Fluent)"""
    return FLUENT_TYPOGRAPHY['font_sizes'].get(size_name, 16)

def obtener_spacing():
    """Obtiene la configuración de espaciado (compatibilidad - ahora usa Fluent)"""
    return FLUENT_SPACING.copy()

def get_spacing(size_name: str) -> int:
    """Obtiene un espaciado específico (compatibilidad - ahora usa Fluent)"""
    # Mapeo de espaciados antiguos a nuevos
    spacing_mapping = {
        'tiny': 'xxs',
        'small': 'xs',
        'medium': 'md',
        'large': 'lg',
        'extra_large': 'xl'
    }
    
    fluent_spacing = spacing_mapping.get(size_name, size_name)
    return FLUENT_SPACING.get(fluent_spacing, 8)

def obtener_elevation():
    """Obtiene la configuración de elevación (compatibilidad - ahora usa Fluent)"""
    return FLUENT_ELEVATION.copy()

def get_border_radius(size_name: str) -> int:
    """Obtiene un radio de borde específico (compatibilidad - ahora usa Fluent)"""
    return FLUENT_ELEVATION['border_radius'].get(size_name, 4)

def get_shadow(depth_name: str) -> str:
    """Obtiene una sombra específica (compatibilidad - ahora usa Fluent)"""
    return FLUENT_ELEVATION['shadows'].get(depth_name, '0 2px 8px rgba(0, 0, 0, 0.3)')

def get_elevation():
    """Obtiene la configuración de elevación (compatibilidad - ahora usa Fluent)"""
    return FLUENT_ELEVATION.copy()