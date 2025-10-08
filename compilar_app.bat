@echo off
echo echo [3/4] Compilando aplicacion...
.\.venv\Scripts\pyinstaller build\TLV_4.0_fixed.spec --distpath="APP TLV COMPILADA"===========================
echo    COMPILADOR TLV 4.0
echo ====================================
echo.

echo [1/4] Limpiando archivos anteriores...
if exist "build" rmdir /s /q "build"
if exist "APP TLV COMPILADA\TLV_4.0.exe" del "APP TLV COMPILADA\TLV_4.0.exe"

echo [2/4] Verificando icono...
if not exist "Images\logo.ico" (
    echo Convirtiendo PNG a ICO...
    .\.venv\Scripts\python convert_icon.py
)

echo [3/4] Compilando aplicacion...
.\.venv\Scripts\pyinstaller --onefile --windowed ^
    --icon="c:\Users\Antware\OneDrive\Desktop\PROYECTOS DEV\TLV_4.0\Images\logo.ico" ^
    --distpath="APP TLV COMPILADA" ^
    --workpath="build" ^
    --specpath="build" ^
    --add-data="app;app" ^
    -n "TLV_4.0" ^
    launcher.py

echo [4/4] Finalizando...
if not exist "APP TLV COMPILADA\data" mkdir "APP TLV COMPILADA\data"

echo.
echo ====================================
echo    COMPILACION COMPLETADA!
echo ====================================
echo.
echo La aplicacion compilada esta en: APP TLV COMPILADA\TLV_4.0.exe
echo.
pause