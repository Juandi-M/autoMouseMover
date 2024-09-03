#!/bin/bash

# Cambiar al directorio del script
cd "$(dirname "$0")"

# Dar permisos de ejecución al script install_caffeinate.sh
chmod +x ./install_caffeinate.sh

# Ejecutar el script de instalación de caffeinate
./install_caffeinate.sh

exit 0