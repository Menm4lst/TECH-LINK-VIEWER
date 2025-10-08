#!/usr/bin/env python3
"""Script para añadir iconos a las categorías"""

# Leer el archivo
with open('app/views/main_window.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Reemplazar la línea con 'Todas'
content = content.replace(
    '        self.lista_categorias.addItem(f"�️ Todas ({total_enlaces})")', 
    '''        item_todas = QListWidgetItem(f"📁 Todas ({total_enlaces})")
        if icono_categoria:
            item_todas.setIcon(icono_categoria)
        self.lista_categorias.addItem(item_todas)'''
)

# Reemplazar la línea del bucle
content = content.replace(
    '            self.lista_categorias.addItem(f"� {categoria} ({count})")', 
    '''            item_categoria = QListWidgetItem(f"📂 {categoria} ({count})")
            if icono_categoria:
                item_categoria.setIcon(icono_categoria)
            self.lista_categorias.addItem(item_categoria)'''
)

# Escribir el archivo actualizado
with open('app/views/main_window.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Archivo actualizado con iconos de categorías')