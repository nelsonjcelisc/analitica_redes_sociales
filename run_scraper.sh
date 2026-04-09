#!/bin/bash
# Ir a la carpeta del proyecto
cd /mnt/data/runtime/analitica_redes_sociales
# Activar el venv usando la ruta completa
source /mnt/data/runtime/analitica_redes_sociales/venv/bin/activate
# Ejecutar el script
python3 src/main.py >> /mnt/data/runtime/analitica_redes_sociales/logs/cron_output.log 2>&1