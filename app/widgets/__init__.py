#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Widgets personalizados para TECH LINK VIEWER
"""

from .titlebar import TitleBar
from .about_dialog import AboutDialog
from .notes_widget import NotesWidget
from .grupos_sn_widget import GruposSNWidget
from .favoritos_widget import FavoritosWidget, FavoritoItemWidget  # ⭐ Nuevo widget de favoritos
from .toast_notification import (
    ToastNotification, ToastManager, ToastType,
    init_toast_system, show_success_toast, show_error_toast,
    show_warning_toast, show_info_toast
)

__all__ = [
    'TitleBar', 'AboutDialog', 'NotesWidget', 'GruposSNWidget',
    'FavoritosWidget', 'FavoritoItemWidget',  # ⭐ Nuevos widgets
    'ToastNotification', 'ToastManager', 'ToastType',
    'init_toast_system', 'show_success_toast', 'show_error_toast',
    'show_warning_toast', 'show_info_toast'
]