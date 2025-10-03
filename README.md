# 🔗 TECH LINK VIEWER

**Una aplicación de escritorio moderna para gestionar, organizar y buscar enlaces web con estilo.**

## ✨ Características Principales

- **🎨 Tema Oscuro Profesional**: Interfaz moderna optimizada para largas sesiones de trabajo
- **🔍 Búsqueda Inteligente**: Búsqueda case-insensitive con soporte para fuzzy matching
- **📁 Gestión de Categorías**: Panel lateral intuitivo para organizar enlaces
- **🏷️ Sistema de Tags**: Etiquetado flexible con filtros de un clic
- **⚡ Apertura Rápida**: Doble clic o Enter para abrir enlaces instantáneamente
- **💾 Persistencia JSON**: Almacenamiento local con funciones de importar/exportar
- **⌨️ Atajos de Teclado**: Navegación completa sin mouse
- **🛡️ Validación Robusta**: Control de URLs duplicadas y validación de datos

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
│   │   ├── main_window.py   # Ventana principal
│   │   └── link_dialog.py   # Diálogo de edición
│   └── utils/
│       ├── __init__.py
│       ├── io.py           # Utilidades de E/S
│       ├── validators.py   # Validadores
│       └── time.py         # Utilidades de tiempo
├── data/
│   └── links.json          # Base de datos JSON
├── requirements.txt
└── README.md
```

## Uso

### Atajos de teclado

- **Ctrl+N**: Nuevo enlace
- **Ctrl+E**: Editar enlace seleccionado
- **Del**: Eliminar enlace seleccionado
- **Ctrl+S**: Guardar datos
- **Ctrl+F**: Enfocar barra de búsqueda
- **Enter**: Abrir enlace seleccionado
- **Esc**: Limpiar búsqueda

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