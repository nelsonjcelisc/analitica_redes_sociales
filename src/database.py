import os
from pymongo import MongoClient
from datetime import datetime

class SocialDatabase:
    def __init__(self):
        # Usamos la URI definida en el docker-compose
        mongo_uri = os.getenv("MONGO_URI", "mongodb://mongodb:27017/")
        self.client = MongoClient(mongo_uri)
        self.db = self.client["social_analytics"]
        self.collection = self.db["tweets"]

    def save_tweet(self, account_label, tweet_data):
        """
        Guarda un tweet o actualiza las cuentas que lo han visto.
        """
        query = {"tweet_id": tweet_data["tweet_id"]}
        
        # Estructura del documento para facilitar la analítica cruzada
        update = {
            "$set": {
                "content": tweet_data["content"],
                "author": tweet_data["author"],
                "timestamp_posted": tweet_data["timestamp_posted"]
            },
            "$addToSet": { "seen_by_accounts": account_label }, # Evita duplicados en la lista
            "$push": { "detection_history": {
                "account": account_label,
                "detected_at": datetime.utcnow()
            }}
        }
        
        self.collection.update_one(query, update, upsert=True)

    def check_connection(self):
        try:
            self.client.admin.command('ping')
            return True
        except Exception as e:
            print(f"Error conectando a MongoDB: {e}")
            return False