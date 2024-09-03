import os
import shutil

# Asume que el directorio actual es 'mac'
base_dir = os.getcwd()

# Define las rutas para 'release'
release_dir = os.path.join(base_dir, 'release')
build_path = os.path.join(release_dir, 'build')
dist_path = os.path.join(release_dir, 'dist')

a = Analysis(
    [os.path.join(base_dir, 'app', 'main.py')],
    pathex=[base_dir],
    binaries=[],
    datas=[
        (os.path.join(base_dir, 'app', 'lang'), 'lang'),  # Incluir toda la carpeta lang
        (os.path.join(base_dir, 'assets', 'icons', 'MouseMoverIcon.icns'), '.'),  # Icono
        (os.path.join(base_dir, 'assets', 'package', 'LICENSE.txt'), 'package'),  # Archivo de licencia
        (os.path.join(base_dir, 'assets', 'package', 'README.MD'), 'package'),  # Archivo README
        (os.path.join(base_dir, 'assets', 'package', 'background.png'), 'package'),  # Imagen de fondo
        (os.path.join(base_dir, 'assets', 'package', 'distribution.xml'), 'package'),  # XML de distribución
        (os.path.join(base_dir, 'scripts', 'install_caffeinate.sh'), '_internal'),  # Script pre-instalación
    ],
    hiddenimports=['pkg_resources', 'setuptools', 'pkg_resources.extern'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    workpath=build_path,  # Ruta 'build' bajo 'release'
    distpath=dist_path,   # Ruta 'dist' bajo 'release'
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MouseMoverApp',
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
    icon=os.path.join(base_dir, 'assets', 'icons', 'MouseMoverIcon.icns'),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MouseMoverApp',
)

app = BUNDLE(
    coll,
    name='MouseMoverApp.app',
    icon=os.path.join(base_dir, 'assets', 'icons', 'MouseMoverIcon.icns'),
    bundle_identifier='com.calenbookai.MouseMoverApp',
    info_plist=os.path.join(base_dir, 'assets', 'package', 'info.plist'),
)

# Mover las carpetas 'build' y 'dist' a 'release' después de la construcción
if not os.path.exists(release_dir):
    os.makedirs(release_dir)

shutil.move(os.path.join(base_dir, 'build'), build_path)
shutil.move(os.path.join(base_dir, 'dist'), dist_path)
