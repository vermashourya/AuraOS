# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('api.py', '.'), ('logger.py', '.'), ('startup.py', '.'), ('tray.py', '.'), ('conversations.json', '.'), ('icon.png', '.'), ('tracker', 'tracker'), ('brain', 'brain'), ('voice', 'voice')]
binaries = []
hiddenimports = ['uvicorn', 'uvicorn.logging', 'uvicorn.loops', 'uvicorn.loops.auto', 'uvicorn.protocols', 'uvicorn.protocols.http', 'uvicorn.protocols.http.auto', 'uvicorn.protocols.websockets', 'uvicorn.protocols.websockets.auto', 'uvicorn.lifespan', 'uvicorn.lifespan.on', 'fastapi', 'fastapi.middleware', 'fastapi.middleware.cors', 'fastapi.responses', 'fastapi.routing', 'fastapi.staticfiles', 'starlette', 'starlette.middleware', 'starlette.middleware.cors', 'starlette.routing', 'starlette.responses', 'starlette.requests', 'starlette.background', 'starlette.datastructures', 'starlette.exceptions', 'starlette.status', 'starlette.types', 'pydantic', 'pydantic.v1', 'pythoncom', 'wmi', 'psutil', 'pycaw', 'whisper', 'edge_tts', 'pystray', 'PIL', 'requests', 'bs4', 'ddgs']
tmp_ret = collect_all('fastapi')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('starlette')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['launcher.py'],
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
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='auraos_backend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='auraos_backend',
)
