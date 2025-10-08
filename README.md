# 🔗 TECH LINK VIEWER 4.0

**Una aplicación de escritorio moderna para gestionar enlaces web, notas personales y grupos de Service Now con estilo profesional.**

## ✨ Características Principales

- **🎨 Tema Oscuro Profesional**: Interfaz moderna optimizada para largas sesiones de trabajo
- **� Sistema de Notificaciones Toast**: Feedback visual inmediato con diseño Fluent moderno
- **�🔍 Búsqueda Inteligente**: Búsqueda case-insensitive con soporte para fuzzy matching en todas las secciones
- **📁 Gestión de Categorías**: Panel lateral intuitivo para organizar enlaces
- **🏷️ Sistema de Tags**: Etiquetado flexible con filtros de un clic
- **📝 Editor de Notas**: Sistema completo de notas con auto-guardado y búsqueda
- **📋 Grupos Service Now**: Gestión integral de grupos SN con información detallada
- **⌨️ Atajos de Teclado**: Flujo de trabajo optimizado con shortcuts profesionales
- **🚀 Guía Paso a Paso**: Sistema de ayuda integrado con F1 (ayuda rápida) y F2 (guía completa)
- **⚡ Apertura Rápida**: Doble clic o Enter para abrir enlaces instantáneamente
- **💾 Persistencia JSON**: Almacenamiento local con funciones de importar/exportar
- **⌨️ Atajos de Teclado**: Navegación completa sin mouse
- **🛡️ Validación Robusta**: Control de URLs duplicadas y validación de datos
- **📝 Sistema de Notas Integrado**: Toma, organiza y gestiona notas con auto-guardado
- **🗂️ Interface con Pestañas**: Navegación entre Enlaces y Notas

## 🚀 Instalación y Ejecución

### Requisitos del Sistema
- **Python 3.11+**
- **Windows 10/11** (optimizado para Windows)

### Configuración Rápida

1. **Clonar o descargar el proyecto**:
   ```bash
   git clone https://github.com/tu-usuario/tech-link-viewer.git
   cd tech-link-viewer
   ```

2. **Crear entorno virtual**:
   ```bash
   python -m venv .venv
   ```

3. **Activar entorno**:
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

4. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Ejecutar aplicación**:
   ```bash
   python -m app.main
   ```

### 🎯 Generar Datos de Demostración

Para probar la aplicación con enlaces de ejemplo:

```bash
python generar_demo.py
```

Esto agregará enlaces tecnológicos organizados en múltiples categorías.

## 📝 Sistema de Notas Integrado

### ¿Qué es?
Una funcionalidad completamente nueva que permite tomar, organizar y gestionar notas directamente en la aplicación, eliminando la necesidad de usar archivos .txt externos.

### Características del Sistema de Notas
- **📋 Interface con pestañas**: Navega entre Enlaces y Notas
- **💾 Auto-guardado inteligente**: Guardado automático cada 3 segundos
- **🔍 Búsqueda en tiempo real**: Busca en títulos y contenido de todas las notas
- **✏️ Editor profesional**: Fuente monospace optimizada para código y texto
- **📊 Gestión completa**: Crear, editar, duplicar y eliminar notas
- **🗂️ Almacenamiento JSON**: Persistencia local con backup automático

### Atajos Específicos de Notas
- **Ctrl+1**: Cambiar a pestaña Enlaces
- **Ctrl+2**: Cambiar a pestaña Notas  
- **Ctrl+Shift+N**: Nueva nota (desde cualquier pestaña)
- **Ctrl+S**: Guardar nota actual
- **Del**: Eliminar nota seleccionada

### ¿Por qué usar el Sistema de Notas?
✅ **Todo centralizado** en una aplicación  
✅ **Búsqueda instantánea** en todas las notas  
✅ **Auto-guardado inteligente** sin pérdidas  
✅ **Interface profesional** con tema oscuro  
✅ **Integración completa** con gestión de enlaces  

👉 **[Ver documentación completa del sistema de notas →](NOTAS.md)**

## 🔔 Sistema de Notificaciones Toast

### ¿Qué son los Toasts?
Un sistema moderno de notificaciones visuales que proporciona **feedback inmediato** al usuario mediante notificaciones elegantes y no intrusivas que aparecen temporalmente en la pantalla.

### ✨ Características del Sistema Toast
- **🎨 Diseño Microsoft Fluent**: Notificaciones con efectos de blur y sombras realistas
- **🚦 4 Tipos de Notificación**: Éxito, Error, Advertencia e Información con colores distintivos
- **⚡ Animaciones Suaves**: Entrada y salida con easing curves profesionales
- **⏱️ Auto-hide Inteligente**: Duración personalizable según el tipo de mensaje
- **📍 Posicionamiento Flexible**: Top-right, top-left, bottom-right, etc.
- **🔄 Sistema de Cola**: Gestión automática de múltiples notificaciones simultáneas

### 🎯 Integración en la Aplicación
Los toasts aparecen automáticamente para todas las acciones importantes:

```
💾 Datos guardados correctamente          ← Al guardar
🔗 Enlace 'GitHub' creado                ← Al crear enlaces  
🗑️ Enlace 'Tutorial' eliminado          ← Al eliminar
📥 Datos importados correctamente        ← Al importar JSON
⚠️ URL duplicada detectada              ← Validaciones
❌ Error al conectar con servidor        ← Errores críticos
```

### 🧪 Demo Interactivo
```bash
# Probar todas las funcionalidades del sistema
python demo_toasts.py
```

👉 **[Ver documentación técnica completa →](docs/TOAST_SYSTEM.md)**

## 🎨 Interfaz y Diseño

### Tema Oscuro Profesional
- **Colores optimizados** para reducir fatiga visual
- **Tipografía moderna** con Segoe UI
- **Elementos interactivos** con efectos hover y focus
- **Paleta de colores** coherente en toda la aplicación

### Componentes Visuales
- **Barra de búsqueda** con placeholder animado
- **Botones modernos** con esquinas redondeadas
- **Tabla responsive** con filas alternadas
- **Panel lateral** de categorías con contadores
- **Barra de estado** informativa
- **Diálogos modales** con validación visual

### Branding
- **TECH LINK VIEWER** - Nombre prominente en la interfaz
- **Iconografía consistente** con emojis y símbolos
- **Versión v4.0.1** - Información de versión integrada

```
TLV_4.0/
├── app/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada
│   ├── ui_main.py           # Interfaz principal
│   ├── models/
│   │   ├── __init__.py
│   │   ├── repository.py    # Gestión de datos JSON
│   │   ├── link_model.py    # Modelo de tabla QAbstractTableModel
│   │   └── search.py        # Motor de búsqueda fuzzy
│   ├── views/
│   │   ├── __init__.py
│   │   ├── main_window.py   # Ventana principal (con tabs)
│   │   └── link_dialog.py   # Diálogo de edición
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── titlebar.py      # Header con efecto typewriter
│   │   ├── about_dialog.py  # Diálogo "Acerca de"
│   │   └── notes_widget.py  # Sistema de notas completo
│   ├── theme/
│   │   ├── __init__.py
│   │   ├── colors.py        # Paleta de colores terminal
│   │   ├── fonts.py         # Configuración de fuentes
│   │   ├── icons.py         # Iconos SVG
│   │   ├── dark.qss         # Estilos CSS de Qt
│   │   └── apply.py         # Aplicador de tema
│   ├── delegates/
│   │   ├── __init__.py
│   │   └── tag_delegate.py  # Renderizado de tags
│   └── utils/
│       ├── __init__.py
│       ├── io.py           # Utilidades de E/S
│       ├── validators.py   # Validadores
│       └── time.py         # Utilidades de tiempo
├── data/
│   ├── links.json          # Base de datos de enlaces
│   └── notas.json          # Base de datos de notas
├── docs/
│   ├── COMPILACION.md      # Guía de compilación
│   ├── INSTALL.md          # Guía de instalación
│   └── NOTAS.md            # Documentación del sistema de notas
├── scripts/
│   ├── compilar.bat        # Script de compilación Windows
│   ├── compilar.sh         # Script de compilación Linux/Mac
│   └── instalar.bat        # Script de instalación Windows
├── requirements.txt
└── README.md
```

## Uso

### Atajos de teclado

#### Navegación General
- **Ctrl+1**: Cambiar a pestaña Enlaces
- **Ctrl+2**: Cambiar a pestaña Notas
- **F1**: Mostrar ayuda
- **F5**: Refrescar datos

#### Gestión de Enlaces
- **Ctrl+N**: Nuevo enlace
- **Ctrl+E**: Editar enlace seleccionado
- **Del**: Eliminar enlace seleccionado
- **Ctrl+S**: Guardar datos
- **Ctrl+F**: Enfocar barra de búsqueda
- **Enter**: Abrir enlace seleccionado
- **Esc**: Limpiar búsqueda

#### Sistema de Notas
- **Ctrl+Shift+N**: Nueva nota (desde cualquier pestaña)
- **Ctrl+N**: Nueva nota (en pestaña de notas)
- **Ctrl+S**: Guardar nota actual
- **Del**: Eliminar nota (con confirmación)

### Funcionalidades

1. **Añadir enlaces**: Botón "Añadir" o Ctrl+N
2. **Buscar**: Escribe en la barra superior (busca en título, URL, categoría y tags)
3. **Filtrar por categoría**: Clic en categoría del panel izquierdo
4. **Filtrar por tag**: Clic en cualquier tag de la tabla
5. **Abrir enlaces**: Doble clic en fila o Enter
6. **Importar/Exportar**: Botones en la barra superior

### Validaciones

- URLs deben comenzar con http:// o https://
- No se permiten URLs duplicadas
- Título es obligatorio
- Categoría es obligatoria

## Empaquetado (Opcional)

Para crear un ejecutable standalone:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed app/main.py
```

## Casos de prueba manuales

### Checklist de funcionalidades:

- [ ] **Inicio**: La aplicación arranca y muestra enlaces de ejemplo
- [ ] **Búsqueda**: Buscar "google" encuentra el enlace de Google
- [ ] **Filtro por categoría**: Seleccionar "Personal" muestra solo enlaces personales
- [ ] **Filtro por tag**: Clic en tag "google" filtra por ese tag
- [ ] **Nuevo enlace**: Ctrl+N abre diálogo, añadir enlace válido
- [ ] **Validación URL**: Intentar URL sin http:// muestra error
- [ ] **URL duplicada**: Intentar añadir URL existente muestra error
- [ ] **Editar enlace**: Ctrl+E o doble clic edita enlace seleccionado
- [ ] **Eliminar enlace**: Del elimina enlace con confirmación
- [ ] **Abrir enlace**: Enter o doble clic abre URL en navegador
- [ ] **Gestión categorías**: Añadir/renombrar/eliminar categorías
- [ ] **Persistencia**: Cerrar y reabrir mantiene cambios
- [ ] **Importar/Exportar**: Exportar JSON e importar en nueva instancia
- [ ] **Navegación teclado**: Tab, Enter, flechas navegan la interfaz
- [ ] **Búsqueda fuzzy**: Buscar "gogle" encuentra "Google"
- [ ] **Insensible a acentos**: Buscar "categoría" encuentra "categoria"

## Arquitectura

- **Patrón MVC**: Separación clara entre modelo, vista y controlador
- **QAbstractTableModel**: Modelo personalizado para tabla optimizada
- **Búsqueda fuzzy**: Algoritmo personalizado de coincidencia difusa
- **Validación robusta**: URLs, duplicados y campos obligatorios
- **Persistencia segura**: Bloqueo de archivos con portalocker

## Logging

Los logs se guardan en `app.log` con información de:
- Operaciones de archivo
- Errores de validación
- Acciones del usuario
- Errores de sistema

## Licencia

Este proyecto es de código abierto bajo licencia MIT.