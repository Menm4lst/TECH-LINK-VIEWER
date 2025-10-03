@echo off
echo ==========================================
echo  TECH LINK VIEWER 4.0 - INSTALADOR
echo  Desarrollado por Antware
echo ==========================================
echo.
echo Este script instalará automáticamente:
echo - Python (si no está instalado)
echo - Dependencias necesarias
echo - TECH LINK VIEWER 4.0
echo.
pause

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no detectado
    echo.
    echo 📥 Descargando Python...
    echo Abriendo página de descarga de Python...
    start https://www.python.org/downloads/
    echo.
    echo Por favor:
    echo 1. Descarga e instala Python
    echo 2. ✅ Marca "Add Python to PATH"
    echo 3. Reinicia este script
    pause
    exit /b 1
)

echo ✅ Python detectado
python --version

REM Crear entorno virtual
echo 📦 Configurando entorno...
if not exist .venv (
    python -m venv .venv
)

REM Activar entorno virtual
call .venv\Scripts\activate.bat

REM Instalar dependencias
echo 📋 Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt

REM Probar la aplicación
echo 🚀 Iniciando TECH LINK VIEWER 4.0...
python -m app.main

echo.
echo ✅ Instalación completada
echo.
echo Para ejecutar en el futuro:
echo 1. Abrir terminal en esta carpeta
echo 2. Ejecutar: .venv\Scripts\activate
echo 3. Ejecutar: python -m app.main
echo.
echo O usar: compilar.bat para crear ejecutable
echo.
pause