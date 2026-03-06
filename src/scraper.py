import os
import logging
import time
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_x_feed(session_path: str, num_tweets: int = 15) -> list[dict]:
    results = []

    if not os.path.exists(session_path):
        logging.error(f"No se encontró el archivo de sesión en '{session_path}'.")
        return results

    try:
        with sync_playwright() as p:
            # Importante: X detecta comportamientos automatizados. 
            # Lanzamos chromium con un user_agent estándar.
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                storage_state=session_path,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            logging.info(f"Navegando a X con sesión: {session_path}")
            page.goto("https://x.com/home", wait_until="domcontentloaded")

            #1. Espera extra para conexiones lentas o renderizado pesado
            time.sleep(10) 

            # 2. CAPTURA DE PANTALLA (Crucial para Nelson)
            # Esto guardará una imagen en tu carpeta data/ de lo que ve el bot
            screenshot_path = "/app/data/debug_x.png"
            page.screenshot(path=screenshot_path)
            logging.info(f"📸 Captura de pantalla guardada en {screenshot_path}")

            # 3. Intenta detectar el tweet
            page.wait_for_selector('article[data-testid="tweet"]', timeout=20000)
            
            # Scroll suave para asegurar que carguen los elementos
            page.mouse.wheel(0, 500)
            
            tweet_elements = page.query_selector_all('article[data-testid="tweet"]')[:num_tweets]

            for element in tweet_elements:
                try:
                    # 1. Extraer el ID del tweet (está en el enlace del timestamp)
                    # El enlace suele tener formato /usuario/status/123456789
                    link_element = element.query_selector('a[href*="/status/"]')
                    if not link_element: continue
                    
                    tweet_url = link_element.get_attribute("href")
                    tweet_id = tweet_url.split("/")[-1]

                    # 2. Extraer el Autor
                    author_element = element.query_selector('div[data-testid="User-Name"]')
                    author = author_element.inner_text().split("\n")[1] if author_element else "unknown"

                    # 3. Extraer el Contenido de texto
                    content_element = element.query_selector('div[data-testid="tweetText"]')
                    content = content_element.inner_text() if content_element else ""

                    results.append({
                        "tweet_id": tweet_id,
                        "author": author,
                        "content": content,
                        "timestamp_detected": datetime.utcnow()
                    })
                except Exception as e:
                    logging.warning(f"Error parseando un tweet individual: {e}")
                    continue

            browser.close()
            logging.info(f"Extracción finalizada. {len(results)} tweets obtenidos.")

    except TimeoutError:
        logging.error(f"Timeout: El feed no cargó. ¿Sesión expirada en {session_path}?")
    except Exception as e:
        logging.error(f"Error inesperado: {e}")

    return results