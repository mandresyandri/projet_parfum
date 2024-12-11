import os
import json
from datetime import datetime
from Scrapper import Scrapper, Parser


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

# if "nocibe.json" not in os.listdir("scrapper/data/current/"):
#     nocibe_parser.parse_pages()

# # # # # # # # # # # # # # # # 
# Scrapper et parser Sephora  #
# # # # # # # # # # # # # # # #

# Appel des objets scrapper et parser
sephora_scrapper = Scrapper(urls["sephora"], "scrapper/data/current/sephora", name="sephora", configs=configs)
sephora_parser = Parser("scrapper/data/current/sephora", "sephora", configs=configs)

if f"sephora_{datetime.now().strftime("%d-%m-%Y")}.html" not in os.listdir("scrapper/data/current/"):
    sephora_scrapper.savehtml()

# if "sephora.json" not in os.listdir("scrapper/data/current/"):
#     sephora_parser.parse_pages()

# # # # # # # # # # # # # # # # #
# Scrapper et parser marionnaud #
# # # # # # # # # # # # # # # # #

# Appel des objets scrapper et parser
marionnaud_scrapper = Scrapper(urls["marionnaud"], "scrapper/data/current/marionnaud", name="marionnaud", configs=configs)
marionnaud_parser = Parser("scrapper/data/current/marionnaud", "marionnaud", configs=configs)

if f"marionnaud_{datetime.now().strftime("%d-%m-%Y")}.html" not in os.listdir("scrapper/data/current/"):
    marionnaud_scrapper.savehtml()

# if "marionnaud.json" not in os.listdir("scrapper/data/current/"):
#     marionnaud_parser.parse_pages()
