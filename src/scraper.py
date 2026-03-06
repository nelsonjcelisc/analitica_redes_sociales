import os
import logging
import time
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_x_feed(session_path: str, num_tweets: int = 15) -> list[dict]:
    results = []
    
    # Aseguramos que la carpeta de sesiones exista
    os.makedirs(os.path.dirname(session_path), exist_ok=True)

    with sync_playwright() as p:
        # Lanzamos HEADLESS=FALSE para que puedas ver y loguearte si es necesario
        # En Linux/Ubuntu (Flappy) esto abrirá una ventana de Chromium
        browser = p.chromium.launch(headless=True) 
        
        # Intentamos cargar el estado si existe
        if os.path.exists(session_path):
            context = browser.new_context(storage_state=session_path)
            logging.info(f"Cargando sesión existente: {session_path}")
        else:
            context = browser.new_context()
            logging.info("No se encontró sesión. Por favor, inicia sesión manualmente en la ventana.")

        page = context.new_page()
        page.goto("https://x.com/home")

        try:
            # Esperamos a ver un tweet. Si no aparece en 30s, asumimos que necesitas loguearte.
            logging.info("Esperando validación de feed (tienes 60s para loguearte si es necesario)...")
            page.wait_for_selector('article[data-testid="tweet"]', timeout=60000)
            
            # --- ¡MAGIA! Guardamos el estado una vez logueados ---
            context.storage_state(path=session_path)
            logging.info(f"✅ Sesión guardada/actualizada en {session_path}")

            # Scroll y extracción
            page.mouse.wheel(0, 1000)
            time.sleep(2)
            
            tweet_elements = page.query_selector_all('article[data-testid="tweet"]')[:num_tweets]
            logging.info(f"Extrayendo {len(tweet_elements)} tweets...")

            for element in tweet_elements:
                try:
                    # ID del Tweet
                    link_element = element.query_selector('a[href*="/status/"]')
                    if not link_element: continue
                    tweet_id = link_element.get_attribute("href").split("/")[-1]

                    # Autor
                    author_el = element.query_selector('div[data-testid="User-Name"]')
                    author = author_el.inner_text().split("\n")[1] if author_el else "unknown"

                    # Texto
                    content_el = element.query_selector('div[data-testid="tweetText"]')
                    content = content_el.inner_text() if content_el else ""

                    results.append({
                        "tweet_id": tweet_id,
                        "author": author,
                        "content": content,
                        "timestamp_posted": datetime.utcnow().isoformat(), # Cambiamos el nombre aquí
                        "timestamp_detected": datetime.utcnow().isoformat() 
                    })
                except Exception as e:
                    continue

        except TimeoutError:
            logging.error("No se pudo cargar el feed. ¿Te logueaste correctamente?")
        finally:
            browser.close()

    return results