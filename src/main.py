import os
import json
from database import SocialDatabase
from scraper import scrape_x_feed
from datetime import datetime

def load_accounts():
    # Buscamos el archivo un nivel arriba de donde está el script
    path = os.path.join(os.path.dirname(__file__), '..', 'accounts.json')
    with open(path, 'r') as f:
        return json.load(f)['accounts']

def main():
    db = SocialDatabase()
    if not db.check_connection():
        return

    accounts = load_accounts()

    # En src/main.py
    for acc in accounts:
        print(f"--- Iniciando recolección para: {acc['label']} ---")
        try:
            # 1. Obtener tweets
            tweets_found = scrape_x_feed(session_path=acc['session_file'], num_tweets=15)
            
            # 2. Guardar en MongoDB
            if tweets_found:
                print(f"DEBUG: Intentando guardar {len(tweets_found)} tweets en Mongo...")
                for tweet in tweets_found:
                    # Aquí llamamos a la base de datos
                    db.save_tweet(acc['label'], tweet)
                print(f"✅ Finalizado: {len(tweets_found)} tweets procesados para {acc['label']}.")
            else:
                print("⚠️ No se encontraron tweets para procesar.")
                
        except Exception as e:
            print(f"Error crítico en la cuenta {acc['label']}: {e}")

if __name__ == "__main__":
    main()