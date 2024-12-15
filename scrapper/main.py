import os
import json
from datetime import datetime
from scrapper import Scrapper, Parser
from etl import ETL


# # # # # # # # # # # # # # # #
# Import des fichiers configs #
# # # # # # # # # # # # # # # #

with open("scrapper/configs/site_url.json") as file:
    urls = dict(json.load(file))

with open("scrapper/configs/scrap_config.json") as file:
    configs = dict(json.load(file))

# # # # # # # # # # # # # # # 
# Scrapper et parser Nocibe #
# # # # # # # # # # # # # # # 

# Appel des objets scrapper et parser
nocibe_scrapper = Scrapper(urls["nocibe"], "scrapper/data/current/nocibe", name="nocibe", configs=configs)
nocibe_parser = Parser("scrapper/data/current/nocibe", "nocibe", configs=configs)

if f"nocibe_{datetime.now().strftime("%d-%m-%Y")}.html" not in os.listdir("scrapper/data/current/"):
    nocibe_scrapper.savehtml()

if f"nocibe_{datetime.now().strftime("%d-%m-%Y")}.json" not in os.listdir("scrapper/data/current/"):
    nocibe_parser.save_json()

# # # # # # # # # # # # # # # # 
# Scrapper et parser Sephora  #
# # # # # # # # # # # # # # # #

# Appel des objets scrapper et parser
sephora_scrapper = Scrapper(urls["sephora"], "scrapper/data/current/sephora", name="sephora", configs=configs)
sephora_parser = Parser("scrapper/data/current/sephora", "sephora", configs=configs)

if f"sephora_{datetime.now().strftime("%d-%m-%Y")}.html" not in os.listdir("scrapper/data/current/"):
    sephora_scrapper.savehtml()

if f"sephora_{datetime.now().strftime("%d-%m-%Y")}.json" not in os.listdir("scrapper/data/current/"):
    sephora_parser.save_json()

# # # # # # # # # # # # # # # # #
# Scrapper et parser marionnaud #
# # # # # # # # # # # # # # # # #

# Appel des objets scrapper et parser
marionnaud_scrapper = Scrapper(urls["marionnaud"], "scrapper/data/current/marionnaud", name="marionnaud", configs=configs)
marionnaud_parser = Parser("scrapper/data/current/marionnaud", "marionnaud", configs=configs)
contain_marionnaud_html = list()
contain_marionnaud_json = list()

for f in os.listdir("scrapper/data/current/"):
    if ("marionnaud" in f) and (".json" in f):
        contain_marionnaud_json.append(f)
    
    elif ("marionnaud" in f) and (".html" in f):
        contain_marionnaud_html.append(f)

if (len(contain_marionnaud_html) < 1):
    marionnaud_scrapper.savehtml()

if (len(contain_marionnaud_json) < 1):
    marionnaud_parser.save_json()

# # # # # # # # #
# Lancer l'ETL  #
# # # # # # # # #

etl_instance = ETL()
etl_instance.archive_json()