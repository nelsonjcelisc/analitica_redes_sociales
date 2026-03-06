import os
from pymongo import MongoClient
from datetime import datetime

class SocialDatabase:
    def __init__(self):
        # Si estamos en Docker, usa 'mongodb'. Si estamos local, usa 'localhost'.
        self.mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client["social_analytics"]

    def save_tweet(self, account_label, tweet_data):
        try:
            # Forzamos el nombre de la colección
            collection = self.db["tweets"]
            tweet_data["account_label"] = account_label
            
            # Usamos update_one con upsert para evitar duplicados
            collection.update_one(
                {"tweet_id": tweet_data["tweet_id"]},
                {"$set": tweet_data},
                upsert=True
            )
            # Si llegamos aquí, se guardó. No necesitamos la variable 'result' para confirmar.
            print(f"  [DB] Tweet {tweet_data['tweet_id']} procesado.")
        except Exception as e:
            print(f"  [DB] Error al guardar: {e}")

    def check_connection(self):
        try:
            self.client.admin.command('ping')
            return True
        except Exception as e:
            print(f"Error conectando a MongoDB: {e}")
            return False