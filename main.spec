# -*- mode: python ; coding: utf-8 -*-
import sys

from PyInstaller.utils.hooks import collect_all

datas = [('x86_build/build_id.txt', '.'), ('x86_build/version.txt', '.')]
hiddenimports = []
if sys.platform == "darwin":
    binaries = [('x86_build/Image-ExifTool-13.29/exiftool', 'bin'),
                ('x86_build/Image-ExifTool-13.29/lib', 'bin/lib')]
else:
    binaries = [('x86_build/exiftool-13.29_64/exiftool.exe', 'bin'),
                ('x86_build/exiftool-13.29_64/exiftool_files', 'bin/exiftool_files')]
tmp_ret = collect_all('dateutil')
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]

a = Analysis( # pylint: disable=undefined-variable
    ['src/main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure) # pylint: disable=undefined-variable

exe = EXE( # pylint: disable=undefined-variable
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='iBenthos Geotagging Tool',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='x86_64',
    codesign_identity=None,
    entitlements_file=None,
    icon='logo.icns',
)
coll = COLLECT( # pylint: disable=undefined-variable
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='iBenthos Geotagging Tool',
)
app = BUNDLE( # pylint: disable=undefined-variable
    coll,
    name='iBenthos Geotagging Tool.app',
    icon='logo.icns',
    bundle_identifier=None,
)
