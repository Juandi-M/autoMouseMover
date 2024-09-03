import os

# Assume that the current working directory is 'mac'
base_dir = os.getcwd()
lang_dir = os.path.join(base_dir, 'app', 'lang')

# Manually include language files
lang_files = [
    (os.path.join(lang_dir, 'lang_en.py'), 'app/lang'),
    (os.path.join(lang_dir, 'lang_es.py'), 'app/lang'),
]

a = Analysis(
    [os.path.join(base_dir, 'app', 'main.py')],  # Correct path to main.py
    pathex=[base_dir],
    binaries=[],
    datas=lang_files + [
        (os.path.join(base_dir, 'assets', 'icons', 'MouseMoverIcon.icns'), '.'),  # Icon
        (os.path.join(base_dir, 'assets', 'package', 'LICENSE.txt'), 'package'),  # License file
        (os.path.join(base_dir, 'assets', 'package', 'README.MD'), 'package'),  # Readme file
        (os.path.join(base_dir, 'assets', 'package', 'background.png'), 'package'),  # Background image
        (os.path.join(base_dir, 'assets', 'package', 'distribution.xml'), 'package'),  # Distribution XML
        (os.path.join(base_dir, 'scripts', 'install_caffeinate.sh'), '.'),  # Pre-install script
        (os.path.join(base_dir, 'scripts', 'postinstall.sh'), '.'),  # Post-install script
    ],
    hiddenimports=['pkg_resources', 'setuptools', 'pkg_resources.extern'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

# Create the PYZ archive
pyz = PYZ(a.pure, a.zipped_data)

# Create the EXE
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
    icon=os.path.join(base_dir, 'assets', 'icons', 'MouseMoverIcon.icns'),  # Set the icon
)

# Collect all necessary files into the final bundle
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MouseMoverApp',
)

# Bundle the application with Info.plist and other resources
app = BUNDLE(
    coll,
    name='MouseMoverApp.app',
    icon=os.path.join(base_dir, 'assets', 'icons', 'MouseMoverIcon.icns'),  # Set the icon
    bundle_identifier='com.calenbookai.MouseMoverApp',  # Set your bundle identifier
    info_plist=os.path.join(base_dir, 'assets', 'package', 'info.plist'),  # Path to your custom Info.plist
)
