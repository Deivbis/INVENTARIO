# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['login.py'],
    pathex=['C:\\Users\\ANDRES MB\\Desktop\\PROYEC_SEMA'],
    binaries=[],
    datas=[
        ('C:\\Users\\ANDRES MB\\Desktop\\PROYEC_SEMA\\trasparente.png', '.'), 
        ('C:\\Users\\ANDRES MB\\Desktop\\PROYEC_SEMA\\logo_proyec.png', '.'), 
        ('C:\\Users\\ANDRES MB\\Desktop\\PROYEC_SEMA\\logo_inventory.png', '.'), 
        ('C:\\Users\\ANDRES MB\\Desktop\\PROYEC_SEMA\\inventary.sql', '.'), 
        ('C:\\Users\\ANDRES MB\\Desktop\\PROYEC_SEMA\\reporte\\*', 'reporte'), 
        ('C:\\Users\\ANDRES MB\\Desktop\\PROYEC_SEMA\\historial\\*', 'historial')
    ],
    hiddenimports=[],
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
    name='InventarioApp',
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
    icon=['logo_proyec.ico'],
)
