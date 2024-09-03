from setuptools import setup
import os

# Ruta absoluta al directorio raíz del proyecto
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

APP = ['source/main.py']
DATA_FILES = [
    ('lang', [os.path.join(root_dir, 'lang/lang_en.py'), os.path.join(root_dir, 'lang/lang_es.py')]),  # Ruta absoluta a los archivos de idioma
    ('logs', []),  # Incluye el directorio de logs, aunque esté vacío
    ('', ['install_caffeinate.sh', 'postinstall.sh'])
]
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'MouseMoverIcon.icns',
    'packages': [],
    'includes': ['lang.lang_en', 'lang.lang_es'],  # Asegúrate de incluir los módulos de idioma
    'plist': {
        'CFBundleName': 'AutoMouseMover',
        'CFBundleDisplayName': 'AutoMouseMover',
        'CFBundleIdentifier': 'com.calenbookai.mousemover',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)