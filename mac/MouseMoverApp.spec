from PyInstaller.utils.hooks import collect_data_files, copy_metadata

# Collect language files from the new location inside 'source/lang'
lang_files = collect_data_files(os.path.join('source', 'lang'), include_py_files=True)

a = Analysis(
    ['source/main.py'],
    pathex=[],
    binaries=[],
    datas=lang_files + [
        ('MouseMoverIcon.icns', '.'),  # Include the icon
        ('package/LICENSE.txt', 'package'),
        ('package/README.MD', 'package'),
        ('package/background.png', 'package'),
        ('package/distribution.xml', 'package'),
        ('install_caffeinate.sh', '.'),  # Pre-install script
        ('postinstall.sh', '.'),  # Post-install script
        *copy_metadata('setuptools'),  # Include setuptools metadata
    ],
    hiddenimports=['pkg_resources', 'setuptools', 'pkg_resources.extern'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
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
    icon='MouseMoverIcon.icns',  # Set the icon
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
    icon='MouseMoverIcon.icns',
    bundle_identifier='com.yourcompany.MouseMoverApp',  # Set your bundle identifier
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'CFBundleDisplayName': 'MouseMoverApp',
        'CFBundleName': 'MouseMoverApp',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleIdentifier': 'com.yourcompany.MouseMoverApp',
        'CFBundleIconFile': 'MouseMoverIcon',
    },
)
