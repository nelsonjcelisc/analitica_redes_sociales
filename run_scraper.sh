#!/bin/bash
#!/bin/bash
# Ir a la carpeta del proyecto
cd /mnt/data/runtime/analitica_redes_sociales
# Si ya está arriba, Docker no hace nada. Si está abajo, lo levanta.
/usr/bin/docker compose up -d
sleep 5
# Activar el venv usando la ruta completa
source /mnt/data/runtime/analitica_redes_sociales/venv/bin/activate
# Ejecutar el script
python3 src/main.py >> /mnt/data/runtime/analitica_redes_sociales/logs/cron_output.log 2>&1