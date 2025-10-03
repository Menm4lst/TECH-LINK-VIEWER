#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de tema para TECH LINK VIEWER
Tema oscuro con estética terminal/administrador de sistemas
"""

from .apply import apply_dark_theme, get_theme_info
from .colors import Colors
from .fonts import Fonts
from .icons import Icons, get_icon

__all__ = [
    'apply_dark_theme',
    'get_theme_info', 
    'Colors',
    'Fonts',
    'Icons',
    'get_icon'
]

__version__ = '1.0.0'
__author__ = 'TECH LINK VIEWER'
__description__ = 'Dark terminal theme for PyQt6 applications'