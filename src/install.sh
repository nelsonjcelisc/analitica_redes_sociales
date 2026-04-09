sudo apt update
sudo apt install python3-pip python3-venv
# Creamos un entorno virtual para no ensuciar Docke
python3 -m venv venv
source venv/bin/activate
pip install playwright pymongo
playwright install chromium
# Instalamos las librerías del sistema para que el navegador abra
playwright install-deps