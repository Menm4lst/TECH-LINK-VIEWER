# 🚀 INSTALACIÓN RÁPIDA - TECH LINK VIEWER 4.0

## 📋 Opciones de Instalación

### 🎯 Opción 1: Instalación Automática (Recomendado)

#### Windows
```batch
# Ejecutar como administrador
instalar.bat
```

#### Linux/macOS
```bash
chmod +x compilar.sh
./compilar.sh
```

### 🛠️ Opción 2: Compilar a Ejecutable

#### Windows
```batch
compilar.bat
```

#### Linux/macOS
```bash
chmod +x compilar.sh
./compilar.sh
```

### ⚡ Opción 3: Instalación Manual

```bash
# 1. Crear entorno virtual
python -m venv .venv

# 2. Activar entorno
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # Linux/macOS

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar aplicación
python -m app.main
```

## 📋 Requisitos del Sistema

- **Python**: 3.8+ (recomendado 3.11+)
- **RAM**: 512 MB mínimo
- **Espacio**: 50 MB libres
- **OS**: Windows 10+, macOS 10.14+, Linux Ubuntu 18.04+

## 🔧 Solución de Problemas

### Python no reconocido
1. Instalar Python desde: https://python.org
2. ✅ Marcar "Add Python to PATH"
3. Reiniciar terminal

### Error de permisos (Linux/macOS)
```bash
chmod +x compilar.sh
chmod +x instalar.sh
```

### Dependencias fallan
```bash
pip install --upgrade pip
pip install PyQt6>=6.7.1
```

## 📞 Soporte

**Desarrollador**: Antware  
**Repositorio**: [TECH-LINK-VIEWER](https://github.com/Menm4lst/TECH-LINK-VIEWER)

---
© 2025 Antware - Hecho con ❤️ y ☕