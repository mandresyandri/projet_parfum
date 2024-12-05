import os
import json
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
nocibe_scrapper = Scrapper(urls["nocibe"], "data/current/nocibe", name="nocibe", configs=configs)
nocibe_parser = Parser("data/current/nocibe", "nocibe", configs=configs)

if "nocibe.html" not in os.listdir("data/"):
    nocibe_scrapper.savehtml()

if "nocibe.json" not in os.listdir("data/"):
    nocibe_parser.parse_pages()

# # # # # # # # # # # # # # # # 
# Scrapper et parser Sephora  #
# # # # # # # # # # # # # # # #

# Appel des objets scrapper et parser
sephora_scrapper = Scrapper(urls["sephora"], "data/current/sephora", name="sephora", configs=configs)
sephora_parser = Parser("data/current/sephora", "sephora", configs=configs)

if "sephora.html" not in os.listdir("data/"):
    sephora_scrapper.savehtml()

if "sephora.json" not in os.listdir("data/"):
    sephora_parser.parse_pages()

# # # # # # # # # # # # # # # # #
# Scrapper et parser marionnaud #
# # # # # # # # # # # # # # # # #

# Appel des objets scrapper et parser
marionnaud_scrapper = Scrapper(urls["marionnaud"], "data/current/marionnaud", name="marionnaud", configs=configs)
marionnaud_parser = Parser("data/current/marionnaud", "marionnaud", configs=configs)

if "marionnaud.html" not in os.listdir("data/"):
    marionnaud_scrapper.savehtml()

if "marionnaud.json" not in os.listdir("data/"):
    marionnaud_parser.parse_pages()
