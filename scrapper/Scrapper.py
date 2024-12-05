import re
import json
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService


# # # # # # # # # #
# Step --> Scrap  #
# # # # # # # # # #
class Scrapper:
    # Config base
    def __init__(self, url_input: str, file_output: str, name: str, configs: dict):
        self.url_input = url_input
        self.file_output = file_output + ".html"
        self.file_output2 = file_output + ".json"
        self.name = name
        self.configs = configs
    
    # Config browser
    def config_browser(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
            )
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--incognito")
        return chrome_options
    
    # Config driver 
    def config_driver(self):
        chrome_options = self.config_browser()
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )
        return driver

    # Traitement des cookies
    def cookies(self, driver):
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.configs[self.name]["wait_cookies"]))
        )
        cookies = driver.find_element(By.CSS_SELECTOR, self.configs[self.name]["cookies"])
        cookies.click()
    
    # Récupération des prix par select
    def wait_price(self, driver):
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.configs[self.name]["contenance"]))
        )
        
    # Sauvegarde des pages 
    def savehtml(self):
        url = self.url_input.split("?")[0]
        driver = self.config_driver()
        driver.get(url)
        self.cookies(driver) if (self.name == "sephora") else None
        self.wait_price(driver) if (self.name == "marionnaud") else None
        html_source = driver.page_source
        driver.quit()
        with open(self.file_output, "w", encoding="utf-8") as file:
            file.write(html_source)

# # # # # # # # # #
# Step --> Parse  #
# # # # # # # # # #
class Parser:
    def __init__(self, file_output: str, name: str ,configs: dict):
        self.file_output = file_output + ".html"
        self.file_output2 = file_output + ".json"
        self.name = name
        self.configs = configs

    def parse_pages(self):
        errors = list()
        data = {"contenance": [], "prix": []} 

        # Ouverture du fichier 
        try:
            # with open("data/UGE - D2SN - Python - 241125 - Exercice.html") as file:
            with open(self.file_output) as file:
                content = file.read()
                soup = BeautifulSoup(content, "html.parser")
        except FileNotFoundError:
            errors.append("Etape lecture fichier : Le fichier spécifié est introuvable.")

        # Extraction des contenances
        contenance_elements = soup.select(self.configs[self.name]["contenance"])
        if not contenance_elements:
            errors.append("Etape extraction contenance : La classe contenant la contenance n'a pas été trouvée.")
        else:
            for e in contenance_elements:
                cleaned_text = e.text.replace("\n", "")
                cleaned_text = cleaned_text.strip()
                data["contenance"].append(cleaned_text)

        # Extraction des prix
        prix_elements = soup.select(self.configs[self.name]["prix"])
        if not prix_elements:
            errors.append("Etape extraction prix : La classe contenant les prix n'a pas été trouvée.")
        else:
            for e in prix_elements:
                cleaned_text = e.text.replace(",", ".").replace("€", "").replace("\n", "").replace("(1)", "")
                cleaned_text = cleaned_text.strip()
                data["prix"].append(cleaned_text)

        # Enregristrement du fichier au format json
        with open(self.file_output2, "w") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        
        filename = self.file_output2.split("/")
        if filename[1] not in os.listdir("data/"):
            errors.append(f"Etape enregistrement du fichier {self.file_output2} : le fichier n'a pas été enregistré.")
            
        print("Good" if len(errors) < 1 else f"Erreur : \n{errors}")
