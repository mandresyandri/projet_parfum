import os
import pandas as pd
from datetime import datetime


path = "data/current/"
in_dir = os.listdir("data/current/")
pd_list = list()
for files in os.listdir(path):
    if files.endswith(".json"):
        pd_list.append(pd.read_json(path+files))


if f"data-{datetime.today().strftime('%d-%m-%Y')}.json" in os.listdir("data/current/"):
    in_dir.remove(f"data-{datetime.today().strftime('%d-%m-%Y')}.json")
    for file in in_dir:
        os.remove(os.path.join("data/current/", file))
else:
    # Transform marionnaud
    marionnaud = pd_list[0]
    marionnaud["platform"] = "Marionnaud"

    # Transform nocibe
    nocibe = pd_list[1]
    nocibe["platform"] = "Nocibé"
    nocibe.drop(nocibe.loc[nocibe.contenance.str.contains("200 ml")].index, inplace=True)

    # Transform nocibe
    sephora = pd_list[2]
    sephora["platform"] = "Sephora"
    sephora.drop(sephora.loc[sephora.contenance.str.contains("200 ml")].index, inplace=True)
    sephora["contenance"] = sephora["contenance"].str.replace(" - Rechargeable", "")

    # Concate datas + ajout de la date du jour
    data = pd.concat([marionnaud, nocibe, sephora], ignore_index=True)
    data["date"] = datetime.today().strftime("%d-%m-%Y")
    data["contenance"] = data["contenance"].str.lower()
    data.to_json(f"data/current/data-{datetime.today().strftime('%d-%m-%Y')}.json", force_ascii=False, orient="records")
