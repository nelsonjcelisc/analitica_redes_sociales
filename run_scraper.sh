#!/bin/bash
# Ruta absoluta a tu proyecto
cd /home/nelsonj/coding/analitica_redes_sociales

# Ejecutamos el contenedor (sin el -it para evitar errores de tty)
/usr/bin/docker exec social_analytics_worker python src/main.py >> logs/cron_output.log 2>&1
