# 🛠️ GUÍA DE COMPILACIÓN - TECH LINK VIEWER 4.0

## 📋 Información General

Esta guía te ayudará a compilar **TECH LINK VIEWER 4.0** desde el código fuente hasta obtener un ejecutable distribuible.

## 🎯 Prerrequisitos

### Software Requerido
- **Python**: 3.8 o superior (recomendado 3.11+)
- **Git**: Para clonar el repositorio
- **pip**: Gestor de paquetes de Python (incluido con Python)

### Verificar Instalación
```bash
python --version     # Debe mostrar 3.8+
pip --version       # Verificar pip
git --version       # Verificar git
```

## 📦 Paso 1: Obtener el Código Fuente

### Clonar desde GitHub
```bash
git clone https://github.com/Menm4lst/TECH-LINK-VIEWER.git
cd TECH-LINK-VIEWER
```

### O Descargar ZIP
1. Ir a: https://github.com/Menm4lst/TECH-LINK-VIEWER
2. Click en "Code" → "Download ZIP"
3. Extraer y navegar a la carpeta

## 🔧 Paso 2: Configurar Entorno

### Crear Entorno Virtual
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Instalar Dependencias
```bash
pip install --upgrade pip
pip install PyQt6>=6.7.1
```

### Verificar Instalación
```bash
python -m app.main
```
*La aplicación debería abrirse correctamente*

## 🏗️ Paso 3: Compilar a Ejecutable

### Opción A: PyInstaller (Recomendado)

#### 1. Instalar PyInstaller
```bash
pip install pyinstaller
```

#### 2. Compilación Básica
```bash
pyinstaller --onefile --windowed app/main.py --name TechLinkViewer
```

#### 3. Compilación Optimizada
```bash
pyinstaller ^
  --onefile ^
  --windowed ^
  --name TechLinkViewer ^
  --exclude-module tkinter ^
  --exclude-module matplotlib ^
  --add-data "data;data" ^
  --add-data "app/theme;app/theme" ^
  app/main.py
```

#### 4. Con Especificación Personalizada
Crear archivo `TLV.spec`:
```python
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['app/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('data/', 'data/'),
        ('app/theme/', 'app/theme/')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='TechLinkViewer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

Compilar con especificación:
```bash
pyinstaller TLV.spec
```

### Opción B: cx_Freeze

#### 1. Instalar cx_Freeze
```bash
pip install cx_Freeze
```

#### 2. Crear setup.py
```python
import sys
from cx_Freeze import setup, Executable

# Configuración
build_exe_options = {
    "packages": ["PyQt6", "logging"],
    "include_files": [
        ("data/", "data/"),
        ("app/theme/", "app/theme/")
    ],
    "excludes": ["tkinter", "matplotlib"],
    "optimize": 2
}

# Base para Windows (sin consola)
base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="TechLinkViewer",
    version="4.0.0",
    description="TECH LINK VIEWER 4.0 - Terminal Edition",
    author="Antware",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "app/main.py",
            base=base,
            target_name="TechLinkViewer",
            icon=None
        )
    ]
)
```

#### 3. Compilar
```bash
python setup.py build
```

## 📂 Paso 4: Archivos de Salida

### Estructura Generada
```
dist/
├── TechLinkViewer.exe     # Ejecutable principal (PyInstaller)
└── data/                  # Datos de la aplicación
    └── links.json

# O para cx_Freeze:
build/
└── exe.win-amd64-3.11/
    ├── TechLinkViewer.exe
    ├── data/
    └── lib/
```

### Tamaños Esperados
- **PyInstaller**: ~25-35 MB
- **cx_Freeze**: ~30-45 MB

## 🚀 Paso 5: Distribución

### Crear Paquete Distribuible

#### Script de Empaquetado (Windows)
```batch
@echo off
echo Creando paquete distribuible...

REM Crear carpeta de distribución
mkdir TechLinkViewer_v4.0
copy dist\TechLinkViewer.exe TechLinkViewer_v4.0\
copy README.md TechLinkViewer_v4.0\
copy INSTALL.md TechLinkViewer_v4.0\

REM Crear datos iniciales
mkdir TechLinkViewer_v4.0\data
copy data\links.json TechLinkViewer_v4.0\data\

echo Empaquetado completado en: TechLinkViewer_v4.0\
pause
```

#### Crear Instalador (NSIS - Opcional)
```nsis
; Installer script para TechLinkViewer
!define APPNAME "TechLinkViewer"
!define APPVERSION "4.0.0"
!define APPAUTHOR "Antware"

Name "${APPNAME} ${APPVERSION}"
OutFile "TechLinkViewer_Setup_v4.0.exe"
InstallDir "$PROGRAMFILES\${APPNAME}"

Section "Principal"
    SetOutPath $INSTDIR
    File "dist\TechLinkViewer.exe"
    File /r "data"
    
    CreateDirectory "$SMPROGRAMS\${APPNAME}"
    CreateShortcut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\TechLinkViewer.exe"
    CreateShortcut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\TechLinkViewer.exe"
SectionEnd
```

## 🔍 Solución de Problemas

### Error: "No module named 'PyQt6'"
```bash
pip install PyQt6>=6.7.1
```

### Error: PyInstaller no encontrado
```bash
pip install pyinstaller
# O reinstalar en entorno virtual
```

### Ejecutable muy grande
```bash
# Usar UPX para comprimir
pip install pyinstaller[encryption]
pyinstaller --onefile --windowed --upx-dir="C:\upx" app/main.py
```

### Error: Falta archivos de datos
Asegurar que los archivos estén incluidos:
```python
# En .spec file
datas=[
    ('data/*.json', 'data'),
    ('app/theme/*', 'app/theme')
]
```

### Problema: Antivirus detecta el ejecutable
- Es normal con PyInstaller
- Añadir excepción en antivirus
- O firmar digitalmente el ejecutable

## ⚡ Optimizaciones

### Reducir Tamaño del Ejecutable
```bash
# Excluir módulos innecesarios
--exclude-module tkinter
--exclude-module matplotlib
--exclude-module numpy
--exclude-module scipy

# Usar UPX compression
--upx-dir="path/to/upx"
```

### Mejorar Tiempo de Inicio
```bash
# No usar --onefile para aplicaciones complejas
pyinstaller --windowed app/main.py

# Optimizar imports en el código
# Usar lazy imports donde sea posible
```

## 📋 Scripts de Automatización

### build.bat (Windows)
```batch
@echo off
echo Iniciando compilación de TechLinkViewer 4.0...

REM Activar entorno virtual
call .venv\Scripts\activate.bat

REM Limpiar builds anteriores
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Compilar con PyInstaller
pyinstaller --onefile --windowed --name TechLinkViewer app/main.py

REM Verificar resultado
if exist dist\TechLinkViewer.exe (
    echo ✅ Compilación exitosa!
    echo Ejecutable en: dist\TechLinkViewer.exe
) else (
    echo ❌ Error en compilación
)

pause
```

### build.sh (Linux/macOS)
```bash
#!/bin/bash
echo "Iniciando compilación de TechLinkViewer 4.0..."

# Activar entorno virtual
source .venv/bin/activate

# Limpiar builds anteriores
rm -rf build dist

# Compilar con PyInstaller
pyinstaller --onefile --windowed --name TechLinkViewer app/main.py

# Verificar resultado
if [ -f "dist/TechLinkViewer" ]; then
    echo "✅ Compilación exitosa!"
    echo "Ejecutable en: dist/TechLinkViewer"
    chmod +x dist/TechLinkViewer
else
    echo "❌ Error en compilación"
fi
```

## 📊 Resultados Esperados

### Archivos Generados
- ✅ **TechLinkViewer.exe** - Ejecutable principal
- ✅ **data/links.json** - Base de datos de enlaces
- ✅ Tamaño total: ~30-40 MB
- ✅ Tiempo de inicio: <3 segundos
- ✅ Compatible con Windows 10/11

### Funcionalidades Verificadas
- ✅ Interfaz gráfica carga correctamente
- ✅ Tema oscuro aplicado
- ✅ Header con efecto typewriter
- ✅ Iconos SVG renderizados
- ✅ Sistema de búsqueda funcional
- ✅ Importar/Exportar JSON
- ✅ Todas las funciones de barra de herramientas

---

## 👨‍💻 Desarrollado por Antware

**TECH LINK VIEWER 4.0** - Terminal Edition  
© 2025 - Hecho con ❤️ y ☕

Para más información: [GitHub Repository](https://github.com/Menm4lst/TECH-LINK-VIEWER)