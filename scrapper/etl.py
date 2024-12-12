import os
import json
import subprocess
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from remote_db import Database


class ETL:
    def __init__(self):
        self.now = datetime.today().strftime('%d-%m-%Y')
        self.data_list = list()
        self.path = "scrapper/data/current/"
        self.output_json = f"data-{datetime.today().strftime("%d-%m-%Y")}.json"
    
    # Partie Extract de l'ETL
    def extract(self):
        for files in os.listdir(self.path):
            if files.endswith(".json"):
                self.data_list.append(pd.read_json(self.path+files))

    # Partie Transform de l'ETL
    def transform(self):
        if self.output_json not in os.listdir(self.path):
            marionnaud = self.data_list[1]
            marionnaud["platform"] = "Marionnaud"

            # Transform nocibe
            nocibe = self.data_list[0]
            nocibe["platform"] = "Nocibé"
            nocibe.drop(nocibe.loc[nocibe.contenance.str.contains("200 ml")].index, inplace=True)

            # Transform nocibe
            sephora = self.data_list[2]
            sephora["platform"] = "Sephora"
            sephora.drop(sephora.loc[sephora.contenance.str.contains("200 ml")].index, inplace=True)
            sephora["contenance"] = sephora["contenance"].str.replace(" - Rechargeable", "")

            # Concat datas + ajout de la date du jour
            data = pd.concat([marionnaud, nocibe, sephora], ignore_index=True)
            data["date"] = self.now
            data["contenance"] = data["contenance"].str.lower()
            data.to_json(f"{self.path}data-{self.now}.json", force_ascii=False, orient="records")

    # Partie Load de l'ETL
    def load_database(self):
        for files in os.listdir(self.path):
            if files.startswith("data"):
                with open(self.path + files) as file:
                    dict_data = json.load(file)

        # test de connexion
        load_dotenv()
        login = os.getenv("login")
        password = os.getenv("password")

        # Insertion des données
        my_data = Database(login, password)
        db = my_data.db_connect()
        my_data.db_insert(db, dict_data)

    # Archiver les données
    def archive_json(self):
        self.extract()
        self.transform()
        self.load_database()

        # Partie archivage des données
        for files in os.listdir(self.path):
            if files.startswith("marionnaud"):
                old = self.path + "marionnaud" + "_" + self.now + ".json"
                new = "scrapper/data/historics/json_files/" + "marionnaud" + "_" + self.now + ".json"
        
                os.makedirs(os.path.dirname(new), exist_ok=True)
                process = f"mv {old} {new}"
                subprocess.run(process, shell=True)

            elif files.startswith("nocibe"):
                old = self.path + "nocibe" + "_" + self.now + ".json"
                new = "scrapper/data/historics/json_files/" + "nocibe" + "_" + self.now + ".json"
        
                os.makedirs(os.path.dirname(new), exist_ok=True)
                process = f"mv {old} {new}"
                subprocess.run(process, shell=True)
            
            elif files.startswith("sephora"):
                old = self.path + "sephora" + "_" + self.now + ".json"
                new = "scrapper/data/historics/json_files/" + "sephora" + "_" + self.now + ".json"
        
                os.makedirs(os.path.dirname(new), exist_ok=True)
                process = f"mv {old} {new}"
                subprocess.run(process, shell=True)

        print(f"{'---' * 3}")
        print(f"The cleanned data is load in the database {self.now}")
        print(f"{'---' * 3}")
