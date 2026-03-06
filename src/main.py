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

    for acc in accounts:
        print(f"--- Iniciando recolección para: {acc['label']} ---")
        try:
            # 1. Conectarse a X y obtener tweets
            #tweets_found = scrape_x_feed(acc['username'], acc['password'], num_tweets=15)
            tweets_found = scrape_x_feed(session_path=acc['session_file'], num_tweets=15)
            
            # 2. Guardar en MongoDB
            for tweet in tweets_found:
                db.save_tweet(acc['label'], tweet)
                
            print(f"Finalizado: {len(tweets_found)} tweets procesados para {acc['label']}.")
            
        except Exception as e:
            print(f"Error crítico en la cuenta {acc['label']}: {e}")

if __name__ == "__main__":
    main()