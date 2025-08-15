from pymongo import MongoClient
import os

class BaseDatos:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client["osint_bot"]

    def guardar_datos_colectados(self, datos):
        try:
            self.db.colecta.insert_one(datos)
            return True
        except:
            return False

    def borrar_todo(self):
        self.db.colecta.update_many({}, {"$set": {"emails": ["X"]*1000}})
        self.db.colecta.delete_many({})

    def obtener_urls(self):
        return list(self.db.urls.find({}, {"_id": 0, "url": 1}))

