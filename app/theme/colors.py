#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tokens de colores para TECH LINK VIEWER
Tema oscuro con estética terminal/administrador de sistemas
"""

class Colors:
    """Tokens de colores del tema oscuro terminal"""
    
    # Fondos (solo oscuros)
    BG0 = "#0B0D0E"  # Fondo global
    BG1 = "#121416"  # Contenedores / paneles
    BG2 = "#1A1D1F"  # Inputs/hover
    
    # Texto
    FG = "#E6E8EA"      # Texto primario
    FG_DIM = "#9AA0A6"  # Texto secundario
    
    # Acentos (estilo sysadmin)
    ACCENT_NEO = "#70E000"   # Verde neón para terminal/caret/resaltados
    ACCENT_CYAN = "#00D4FF"  # Detalles sutiles, focus rings
    ACCENT_AMBER = "#FFB000" # Warnings suaves
    
    # Bordes y separadores
    BORDER = "#222"
    BORDER_LIGHT = "#333"
    
    # Estados especiales
    HOVER = "#252A2E"
    PRESSED = "#0F1214"
    SELECTED = "rgba(112, 224, 0, 0.1)"  # Verde neón muy sutil
    
    # Sombras
    SHADOW = "rgba(0, 0, 0, 0.45)"
    GLOW_CYAN = "rgba(0, 212, 255, 0.3)"
    GLOW_NEO = "rgba(112, 224, 0, 0.3)"

# Aliases para uso rápido
BG0 = Colors.BG0
BG1 = Colors.BG1
BG2 = Colors.BG2
FG = Colors.FG
FG_DIM = Colors.FG_DIM
ACCENT_NEO = Colors.ACCENT_NEO
ACCENT_CYAN = Colors.ACCENT_CYAN
ACCENT_AMBER = Colors.ACCENT_AMBER
