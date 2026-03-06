import os
import logging
from database import SocialDatabase
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO)

def test():
    # 1. Probar Mongo
    logging.info("--- Probando MongoDB ---")
    db = SocialDatabase()
    if db.check_connection():
        logging.info("✅ Conexión a MongoDB Exitosa")
    else:
        logging.error("❌ Falló conexión a MongoDB")

    # 2. Probar Playwright (sin login, solo abrir la web)
    logging.info("--- Probando Playwright ---")
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://x.com", wait_until="networkidle", timeout=20000)
            logging.info(f"✅ Playwright alcanzó X.com. Título: {page.title()}")
            browser.close()
        except Exception as e:
            logging.error(f"❌ Playwright falló: {e}")

if __name__ == "__main__":
    test()