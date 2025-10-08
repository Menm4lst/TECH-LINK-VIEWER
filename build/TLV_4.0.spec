# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['..\\launcher.py'],
    pathex=[],
    binaries=[],
    datas=[('../app', 'app')],
    hiddenimports=[
        'app.main',
        'app.views.main_window', 
        'app.models.repository',
        'app.models.link_model',
        'app.theme.fonts',
        'app.widgets.titlebar',
        'app.widgets.about_dialog', 
        'app.widgets.notes_widget',
        'app.widgets.grupos_sn_widget',
        'app.utils',
        'app.config'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='TLV_4.0',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['c:\\Users\\Antware\\OneDrive\\Desktop\\PROYECTOS DEV\\TLV_4.0\\Images\\logo.ico'],
)
