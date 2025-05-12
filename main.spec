# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[('Image-ExifTool-13.29/exiftool', 'bin/exiftool'), ('Image-ExifTool-13.29/lib', 'bin/lib')],
    datas=[('src/main.qml', '.'), ('src/Components', 'Components')],
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
    [],
    exclude_binaries=True,
    name='iBenthos Geotagging Tool',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='logo.png',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='iBenthos Geotagging Tool',
)

app = BUNDLE(
    coll,
    name='iBenthos Geotagging Tool.app',
    icon='logo.png',
    bundle_identifier=None,
)