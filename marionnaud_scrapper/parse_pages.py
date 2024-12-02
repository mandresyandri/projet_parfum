import json
import os
from bs4 import BeautifulSoup

errors = list()
data = {"contenance": [], "prix": []} 

# Ouverture du fichier 
try:
    with open("data/UGE - D2SN - Python - 241125 - Exercice.html") as file:
        content = file.read()
        soup = BeautifulSoup(content, "html.parser")
except FileNotFoundError:
    errors.append("Etape lecture fichier : Le fichier spécifié est introuvable.")

# Extraction des contenances
contenance_elements = soup.find_all("div", class_="abt-var-sel__name")
if not contenance_elements:
    errors.append("Etape extraction contenance : La classe 'abt-var-sel__name' n'est pas trouvée.")
else:
    for e in contenance_elements:
        data["contenance"].append(e.text)

# Extraction des prix
prix_elements = soup.find_all("span", class_="abt-var-sel__new-price")
if not prix_elements:
    errors.append("Etape extraction prix : La classe 'abt-var-sel__new-price' n'est pas trouvée.")
else:
    for e in prix_elements:
        cleaned_text = e.text.replace(",", ".").replace("€", "")
        data["prix"].append(cleaned_text)

# Enregristrement du fichier au format json
with open("data/output_data.json", "w") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

if "output_data.json" not in os.listdir("data/"):
    errors.append("Etape enregistrement du fichier : le fichier n'a pas été enregistré.")