#!/bin/bash

echo "=========================================="
echo " TECH LINK VIEWER 4.0 - COMPILADOR"
echo " Desarrollado por Antware"
echo "=========================================="
echo

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    echo "Instala Python3 primero"
    exit 1
fi

echo "✅ Python3 detectado"
python3 --version

# Verificar si existe entorno virtual
if [ ! -d ".venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "❌ Error creando entorno virtual"
        exit 1
    fi
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source .venv/bin/activate

# Actualizar pip
echo "⬆️ Actualizando pip..."
python -m pip install --upgrade pip

# Instalar dependencias
echo "📋 Instalando dependencias..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Error instalando dependencias"
    exit 1
fi

# Instalar PyInstaller
echo "🛠️ Instalando PyInstaller..."
pip install pyinstaller
if [ $? -ne 0 ]; then
    echo "❌ Error instalando PyInstaller"
    exit 1
fi

# Limpiar builds anteriores
echo "🧹 Limpiando compilaciones anteriores..."
rm -rf build dist

# Compilar aplicación
echo "🏗️ Compilando TechLinkViewer 4.0..."
echo "Esto puede tomar varios minutos..."
pyinstaller \
  --onefile \
  --windowed \
  --name TechLinkViewer \
  --exclude-module tkinter \
  --exclude-module matplotlib \
  --add-data "data:data" \
  --add-data "app/theme:app/theme" \
  app/main.py

# Verificar resultado
if [ -f "dist/TechLinkViewer" ]; then
    echo
    echo "✅ ¡COMPILACIÓN EXITOSA!"
    echo
    echo "📁 Ejecutable generado en: dist/TechLinkViewer"
    ls -lh dist/TechLinkViewer
    echo
    chmod +x dist/TechLinkViewer
    echo "🚀 Para ejecutar: ./dist/TechLinkViewer"
    echo
    read -p "¿Quieres ejecutar la aplicación ahora? (y/n): " respuesta
    if [[ $respuesta == "y" || $respuesta == "Y" ]]; then
        ./dist/TechLinkViewer &
    fi
else
    echo
    echo "❌ ERROR EN LA COMPILACIÓN"
    echo "Revisa los mensajes de error arriba"
    echo
fi

echo
echo "Presiona Enter para salir..."
read