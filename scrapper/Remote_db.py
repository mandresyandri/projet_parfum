from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class Database:
    def __init__(self, login:str, password:str):
        self.login = login
        self.password = password
        self.db_name = "side_project"
        self.coll_name = "projet_parfum"

    # Connexion à la base de données
    def db_connect(self):
        uri = f"mongodb+srv://{self.login}:{self.password}@cluster0.rwi7i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = client[self.db_name][self.coll_name]

        return self.db
    
    # Insérer des données
    def db_insert(self, db, data_dict: dict):
        db.insert_many(data_dict)

    # Afficher les données
    def display_data(self, db):
        collection = self.db
        db_data = collection.find()
        data = {"contenance": [], "prix": [], "platform": [] ,"date": []}
        for rows in db_data:
            data["contenance"].append(rows["contenance"])
            data["prix"].append(rows["prix"])
            data["platform"].append(rows["platform"]) 
            data["date"].append(rows["date"]) 

        return data
