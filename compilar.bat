@echo off
echo ==========================================
echo  TECH LINK VIEWER 4.0 - COMPILADOR
echo  Desarrollado por Antware
echo ==========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado o no está en PATH
    echo Descarga Python desde: https://python.org
    pause
    exit /b 1
)

echo ✅ Python detectado
python --version

REM Verificar si existe entorno virtual
if not exist .venv (
    echo 📦 Creando entorno virtual...
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ Error creando entorno virtual
        pause
        exit /b 1
    )
)

REM Activar entorno virtual
echo 🔧 Activando entorno virtual...
call .venv\Scripts\activate.bat

REM Actualizar pip
echo ⬆️ Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo 📋 Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Error instalando dependencias
    pause
    exit /b 1
)

REM Instalar PyInstaller
echo 🛠️ Instalando PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo ❌ Error instalando PyInstaller
    pause
    exit /b 1
)

REM Limpiar builds anteriores
echo 🧹 Limpiando compilaciones anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Compilar aplicación
echo 🏗️ Compilando TechLinkViewer 4.0...
echo Esto puede tomar varios minutos...
pyinstaller ^
  --onefile ^
  --windowed ^
  --name TechLinkViewer ^
  --exclude-module tkinter ^
  --exclude-module matplotlib ^
  --add-data "data;data" ^
  --add-data "app\theme;app\theme" ^
  app\main.py

REM Verificar resultado
if exist dist\TechLinkViewer.exe (
    echo.
    echo ✅ ¡COMPILACIÓN EXITOSA!
    echo.
    echo 📁 Ejecutable generado en: dist\TechLinkViewer.exe
    dir dist\TechLinkViewer.exe
    echo.
    echo 🚀 Para ejecutar: dist\TechLinkViewer.exe
    echo.
    echo ¿Quieres ejecutar la aplicación ahora? (y/n)
    set /p respuesta=
    if /i "%respuesta%"=="y" (
        start "" "dist\TechLinkViewer.exe"
    )
) else (
    echo.
    echo ❌ ERROR EN LA COMPILACIÓN
    echo Revisa los mensajes de error arriba
    echo.
)

echo.
echo Presiona cualquier tecla para salir...
pause >nul