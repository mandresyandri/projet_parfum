import os
import json
from dotenv import load_dotenv
from Remote_db import Database

path="data/current/"
for files in os.listdir(f"{path}"):
    if files.startswith("data"):
        with open(path + files) as file:
            dict_data = json.load(file)

# test de connexion
load_dotenv()
login = os.getenv("login")
password = os.getenv("password")

# Insertion des données
my_data = Database(login, password)
db = my_data.db_connect()
my_data.db_insert(db, dict_data)
