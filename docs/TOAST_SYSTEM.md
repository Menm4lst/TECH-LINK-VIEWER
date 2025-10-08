# 🔔 Sistema de Notificaciones Toast - TECH LINK VIEWER 4.0

## 📋 Descripción

El sistema de notificaciones toast proporciona feedback visual inmediato al usuario mediante notificaciones elegantes, no intrusivas y modernas que siguen el Microsoft Fluent Design System.

## ✨ Características Principales

### 🎨 **Diseño Fluent**
- **Acrylic Materials** con efectos de desenfoque
- **Colores adaptativos** según el tipo de notificación
- **Animaciones suaves** de entrada y salida con easing curves
- **Sombras realistas** y efectos de profundidad
- **Tipografía Segoe UI Variable** optimizada

### 🔧 **Funcionalidad Avanzada**
- **4 tipos de notificación**: Éxito, Error, Advertencia, Información
- **Auto-hide configurable** con duración personalizable
- **Sistema de cola** para múltiples notificaciones
- **Posicionamiento inteligente** (top-right, top-left, etc.)
- **Botón de cierre opcional**
- **Gestión automática** de notificaciones activas

### 🎯 **Integración Completa**
- **API global simple** para uso en toda la aplicación
- **Manager centralizado** para control avanzado
- **Eventos y señales** para interactividad
- **Compatibilidad total** con PyQt6

## 🚀 Uso Básico

### Funciones Globales (Recomendado)

```python
from app.widgets import (
    show_success_toast, show_error_toast, 
    show_warning_toast, show_info_toast
)

# Notificaciones básicas
show_success_toast("💾 Datos guardados correctamente")
show_error_toast("❌ Error al conectar con el servidor")
show_warning_toast("⚠️ Verifica los datos ingresados")
show_info_toast("ℹ️ Proceso completado")

# Con duración personalizada
show_success_toast("✅ Enlace creado", duration=5000)  # 5 segundos
```

### Inicialización del Sistema

```python
from app.widgets import init_toast_system

class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        # ... configuración de la ventana ...
        
        # Inicializar sistema de toasts (una sola vez)
        init_toast_system(self)
```

## 🔧 Uso Avanzado

### ToastManager Personalizado

```python
from app.widgets import ToastManager, ToastType

class MiWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Crear manager personalizado
        self.toast_manager = ToastManager(self)
        
        # Configurar parámetros específicos
        self.toast_manager.max_toasts = 3  # Max 3 toasts simultáneos
    
    def operacion_compleja(self):
        # Notificación con configuración avanzada
        self.toast_manager.show_success(
            message="Operación completada",
            duration=4000,
            closable=True
        )
```

### Toasts Personalizados

```python
from app.widgets import ToastNotification, ToastType

# Toast completamente personalizado
toast = ToastNotification(
    parent=self,
    message="Mensaje personalizado",
    toast_type=ToastType.SUCCESS,
    duration=3000,
    closable=True,
    position="bottom-right"
)

# Conectar eventos
toast.clicked.connect(self.on_toast_clicked)
toast.closed.connect(self.on_toast_closed)

# Mostrar el toast
toast.show_toast()
```

## 🎨 Tipos de Notificaciones

### ✅ Éxito (SUCCESS)
- **Color**: Verde (`#4CAF50`)
- **Icono**: ✓
- **Uso**: Operaciones completadas exitosamente
- **Duración**: 3 segundos

### ❌ Error (ERROR)
- **Color**: Rojo (`#F44336`)
- **Icono**: ✕
- **Uso**: Errores críticos que requieren atención
- **Duración**: 5 segundos

### ⚠️ Advertencia (WARNING)
- **Color**: Naranja (`#FF9800`)
- **Icono**: ⚠
- **Uso**: Situaciones que requieren precaución
- **Duración**: 4 segundos

### ℹ️ Información (INFO)
- **Color**: Violeta (`#9D4EDD`)
- **Icono**: ℹ
- **Uso**: Información general al usuario
- **Duración**: 3 segundos

## 📍 Posicionamiento

Posiciones disponibles:
- `"top-right"` (por defecto)
- `"top-left"`
- `"bottom-right"`
- `"bottom-left"`
- `"center"`

## ⚙️ Configuración

### Parámetros Globales

```python
# En config.py se pueden ajustar:
TOAST_CONFIG = {
    'max_simultaneous': 5,      # Máximo de toasts simultáneos
    'default_duration': 3000,   # Duración por defecto (ms)
    'position': 'top-right',    # Posición por defecto
    'margin': 20,               # Margen desde los bordes
    'spacing': 10,              # Espaciado entre toasts
    'animation_duration': 300,  # Duración de animaciones (ms)
}
```

### Personalización de Colores

```python
# Los colores se toman automáticamente del sistema Fluent
colors = obtener_fluent_colors()

# Personalizar en config.py:
FLUENT_COLOR_SCHEME = {
    'success': '#4CAF50',    # Verde para éxito
    'error': '#F44336',      # Rojo para error  
    'warning': '#FF9800',    # Naranja para advertencia
    'info': '#9D4EDD',       # Violeta para información
}
```

## 🔄 Integración en la Aplicación

### Acciones CRUD

```python
def _guardar_datos(self):
    if self.repositorio.guardar():
        show_success_toast("💾 Datos guardados correctamente")
    else:
        show_error_toast("❌ Error al guardar los datos")

def _eliminar_enlace(self, titulo):
    if self.repositorio.eliminar(enlace_id):
        show_success_toast(f"🗑️ Enlace '{titulo}' eliminado")
    else:
        show_error_toast("❌ Error al eliminar el enlace")

def _importar_datos(self):
    try:
        resultado = self.repositorio.importar(archivo)
        show_success_toast("📥 Datos importados correctamente")
    except Exception as e:
        show_error_toast("❌ Error al importar archivo")
```

### Validaciones

```python
def _validar_formulario(self):
    if not self.url_field.text():
        show_warning_toast("⚠️ La URL es obligatoria")
        return False
    
    if not self._es_url_valida(self.url_field.text()):
        show_error_toast("❌ Formato de URL inválido")
        return False
    
    show_info_toast("ℹ️ Formulario validado correctamente")
    return True
```

### Operaciones Asíncronas

```python
def _proceso_largo(self):
    show_info_toast("🔄 Iniciando proceso...")
    
    # Simular proceso
    QTimer.singleShot(2000, lambda: show_info_toast("⏳ Procesando datos..."))
    QTimer.singleShot(4000, lambda: show_success_toast("✅ Proceso completado"))
```

## 🧪 Pruebas y Demo

Para probar el sistema de toasts:

```bash
# Ejecutar demo interactivo
python demo_toasts.py

# Ejecutar aplicación principal (con toasts integrados)
python launcher.py
```

## 📚 API Reference

### Funciones Globales

- `init_toast_system(parent_widget)` - Inicializa el sistema global
- `show_success_toast(message, duration=3000)` - Toast de éxito
- `show_error_toast(message, duration=5000)` - Toast de error
- `show_warning_toast(message, duration=4000)` - Toast de advertencia
- `show_info_toast(message, duration=3000)` - Toast informativo

### Clases Principales

- `ToastNotification` - Widget individual de notificación
- `ToastManager` - Gestor de múltiples notificaciones
- `ToastType` - Enum con tipos de notificación

### Eventos

- `clicked` - Usuario hace clic en el toast
- `closed` - Toast se cierra completamente

## 🎯 Mejores Prácticas

### ✅ Recomendado

```python
# Usar emojis para mejor UX
show_success_toast("💾 Archivo guardado")

# Mensajes concisos y claros
show_error_toast("❌ Conexión perdida")

# Información contextual relevante
show_info_toast(f"📊 {total} enlaces cargados")
```

### ❌ Evitar

```python
# Mensajes muy largos
show_error_toast("Error muy largo que no se puede leer bien...")

# Demasiadas notificaciones simultáneas
for i in range(10):
    show_info_toast(f"Mensaje {i}")  # Saturará al usuario

# Sin contexto
show_success_toast("Hecho")  # ¿Qué se hizo exactamente?
```

## 🔧 Solución de Problemas

### Toast no se muestra
- Verificar que `init_toast_system()` fue llamado
- Asegurar que el parent widget existe
- Revisar logs para errores de importación

### Animaciones lentas
- Ajustar `animation_duration` en la configuración
- Verificar hardware gráfico del sistema

### Posicionamiento incorrecto
- Verificar que el parent widget tiene dimensiones válidas
- Usar `show()` en el widget padre antes de mostrar toasts

---

## 🌟 Próximas Mejoras

- **Persistencia** de notificaciones importantes
- **Sonidos** opcionales para cada tipo
- **Temas personalizables** para toasts
- **Integración con sistema de notificaciones** del OS
- **Animaciones avanzadas** (bouncing, scaling)
- **Agrupación inteligente** de notificaciones similares

---

*Sistema implementado como parte de TECH LINK VIEWER 4.0 con Microsoft Fluent Design System*