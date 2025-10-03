# TECH LINK VIEWER - Tema Oscuro Terminal

## Descripción General

TECH LINK VIEWER ha sido completamente refactorizado con un tema oscuro moderno inspirado en terminales y herramientas de administración de sistemas. El diseño mantiene toda la funcionalidad existente mientras proporciona una experiencia visual profesional y moderna.

## Características Implementadas

### 🎨 Identidad Visual

**Paleta de Colores (Dark Only):**
- `bg0: #0B0D0E` - Fondo global (near-black)
- `bg1: #121416` - Contenedores y paneles
- `bg2: #1A1D1F` - Inputs y estados hover
- `fg: #E6E8EA` - Texto primario (high contrast)
- `fg-dim: #9AA0A6` - Texto secundario

**Acentos Estilo SysAdmin:**
- `accent-neo: #70E000` - Verde neón para terminal/caret/resaltados
- `accent-cyan: #00D4FF` - Detalles sutiles, focus rings
- `accent-amber: #FFB000` - Warnings suaves

**Tipografía:**
- Fuente principal: JetBrains Mono (fallback: Cascadia Code, Fira Code, Consolas, monospace)
- Tamaños: 9px (small), 10px (normal), 12px (medium), 14px (large), 18px (header), 20px (title)

### 🔥 Header con Efecto Typewriter

El componente más destacado es el header animado que muestra "TECH LINK VIEWER" con:

- **Efecto de tipeo**: Aparece letra por letra como en una terminal
- **Caret parpadeante**: Cursor █ verde neón que parpadea cada 500ms
- **Ciclo automático**: Escribe → pausa → borra → repite
- **Configuración flexible**: Velocidades, pausas y caracteres personalizables

**Uso del TitleBar:**
```python
from app.widgets import TitleBar

title_bar = TitleBar()
title_bar.configure(
    type_speed=120,      # ms entre caracteres al escribir
    erase_speed=80,      # ms entre caracteres al borrar
    pause_duration=3000, # ms de pausa con texto completo
    erase_pause=500,     # ms antes de empezar a borrar
    caret_char="█",      # carácter del caret
    loop_enabled=True    # loop automático
)
title_bar.start()  # Iniciar animación
```

### 🎯 Componentes Estilizados

**QSS Global aplicado a:**
- `QMainWindow`, `QStatusBar`, `QToolBar` con look minimalista
- `QLineEdit` con focus rings cyan y fondos dark
- `QPushButton` con hover effects y bordes accent
- `QListWidget` para categorías con chips seleccionadas
- `QTableView` con estilo terminal: filas zebra, selection glow
- `QScrollBar` fino con hover effects
- Tags renderizadas como píldoras personalizadas

**Íconos SVG Inline:**
- 6+ íconos incluidos: search, add, edit, delete, import, export
- Estados hover: fg-dim → accent-neo
- Renderizado vectorial limpio y escalable

### 🏗️ Arquitectura del Tema

**Estructura modular:**
```
app/theme/
├── __init__.py          # Exports principales
├── colors.py            # Tokens de colores
├── fonts.py             # Configuración de fuentes
├── icons.py             # Íconos SVG inline
├── dark.qss            # Estilos QSS globales
└── apply.py            # Aplicador de tema

app/widgets/
├── __init__.py
└── titlebar.py         # Widget con typewriter effect

app/delegates/
├── __init__.py
└── tag_delegate.py     # Renderizado de tags como chips
```

### ⚡ Microinteracciones

**Efectos implementados:**
- Hover suave en botones con transiciones de color
- Focus rings visibles en inputs con glow cyan
- Selección en categorías con barra lateral verde neón
- Tags como chips con hover effect
- Estado visual claro para botones enabled/disabled

### 📋 Estados y Accesibilidad

**Contraste AA mínimo** garantizado:
- Texto primario vs fondo: #E6E8EA vs #0B0D0E
- Estados hover, pressed, selected claramente diferenciados
- Focus rings siempre visibles con accent-cyan
- Estados error (amber) y success (neo green)

## Activación del Tema

### Configuración Automática

El tema se aplica automáticamente al iniciar la aplicación:

```python
from app.theme import apply_dark_theme

app = QApplication(sys.argv)
apply_dark_theme(app)  # Aplica tema completo
```

### Configuración Manual

Para uso avanzado o personalización:

```python
from app.theme import Colors, Fonts, DarkTheme
from PyQt6.QtWidgets import QApplication

app = QApplication(sys.argv)

# Aplicar fuentes monoespaciadas
Fonts.apply_global_font(app)

# Aplicar stylesheet
app.setStyleSheet(DarkTheme.get_main_stylesheet())

# Configurar paleta de fallback
# ... (ver app/theme/apply.py)
```

### Personalización del Typewriter

```python
# Configuración rápida
title_bar.configure(type_speed=100, caret_char="▊")

# Configuración completa
title_bar.configure(
    type_speed=150,        # Más lento
    erase_speed=50,        # Borrado más rápido
    pause_duration=5000,   # Pausa más larga
    erase_pause=1000,      # Pausa antes de borrar
    caret_char="▊",        # Caret diferente
    loop_enabled=False     # Sin loop automático
)

# Control programático
title_bar.start()         # Iniciar
title_bar.pause()         # Pausar
title_bar.resume()        # Reanudar
title_bar.stop()          # Detener
```

## Integración Completa

### Aplicación Principal

La ventana principal (`app/views/main_window.py`) ha sido completamente refactorizada:

1. **Header typewriter** reemplaza el título estático anterior
2. **Toolbar minimalista** con íconos SVG hover-reactive
3. **Panel de categorías** simplificado con estilo terminal
4. **Tabla de enlaces** con delegate para tags como chips
5. **Barra de estado** con tema dark consistente

### Compatibilidad

- ✅ Mantiene 100% de la funcionalidad existente
- ✅ Búsqueda difusa, filtros, CRUD operations
- ✅ Importación/exportación JSON
- ✅ Atajos de teclado
- ✅ Validaciones y manejo de errores
- ✅ Compatibilidad con PyQt6 6.7.1+

### Rendimiento

- ⚡ Animaciones optimizadas con QTimer
- ⚡ Renderizado SVG eficiente con cache
- ⚡ Estilos QSS compilados una sola vez
- ⚡ Sin dependencias pesadas adicionales

## Testing y Validación

### Test Manual Incluido

Ejecutar demostración del tema:

```bash
python test_tema_oscuro.py
```

Esto muestra:
- Header con typewriter funcionando
- Íconos con hover effects
- Toda la paleta de colores aplicada
- Fuentes monoespaciadas correctas

### Checklist de Validación

- [x] App corre con tema oscuro sin romper funcionalidad
- [x] Header muestra TECH LINK VIEWER con typewriter loop
- [x] Búsqueda, categorías y tabla mantienen usabilidad
- [x] Tags se ven como chips estilizadas
- [x] Íconos SVG cambian a accent-neo en hover
- [x] Focus rings visibles y contrastes adecuados
- [x] Solo colores oscuros, family blacks/near-black + acentos
- [x] Código modular: theme/, widgets/, delegates/

## Archivos Modificados y Nuevos

### Archivos Nuevos:
- `app/theme/` (módulo completo)
- `app/widgets/titlebar.py`
- `app/delegates/tag_delegate.py`
- `test_tema_oscuro.py`

### Archivos Modificados:
- `app/ui_main.py` - Aplicación del nuevo tema
- `app/views/main_window.py` - Refactorización completa de UI

### Sin Cambios:
- `app/models/` - Lógica de negocio intacta
- `app/utils/io.py` - Operaciones de archivo
- `data/links.json` - Estructura de datos

## Resultado Final

TECH LINK VIEWER ahora presenta una identidad visual profesional y moderna que:

1. **Mejora la experiencia de usuario** con una interfaz elegante y coherente
2. **Mantiene la funcionalidad completa** sin regresiones
3. **Proporciona una base sólida** para futuras mejoras visuales
4. **Refleja profesionalismo** apropiado para herramientas de productividad

La aplicación está lista para usar inmediatamente con `python -m app.main` y proporciona una experiencia visual significativamente mejorada mientras preserva toda la potencia funcional del sistema original.