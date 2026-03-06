FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema para navegadores
RUN apt-get update && apt-get install -y \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 \
    libgbm1 libasound2 libpangocairo-1.0-0 libpango-1.0-0

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar los navegadores de Playwright
RUN playwright install chromium
RUN playwright install-deps chromium

COPY . .

# Comando por defecto (puedes cambiarlo al nombre de tu script)
CMD ["python", "src/main.py"]