import os
import json
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


# # # # # # # # # #
# Step --> Scrap  #
# # # # # # # # # #
class Scrapper:
    # Config base
    def __init__(self, url_input: str, file_output: str, name: str, configs: dict):
        self.url_input = url_input
        self.file_output = file_output
        self.name = name
        self.configs = configs
        self.now = datetime.now().strftime("%d-%m-%Y")
        self.errors = list()
    
    # Config browser
    def config_browser(self):
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
                )
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument("--incognito")
            return chrome_options
        except:
            self.errors.append("Erreur étape : Configuration du webdriver")
    
    # Config driver 
    def config_driver(self):
        try:
            chrome_options = self.config_browser()
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=chrome_options
            )
            return driver
        except:
            self.errors.append("Erreur étape : Configuration du driver")
    
    # Ingorer les cookies
    def skip_cookies(self, driver):
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.configs[self.name]["cookies"]))
            )
            cookies = driver.find_element(By.CSS_SELECTOR, self.configs[self.name]["cookies"])
            cookies.click()
        except:
            self.errors.append("Erreur étape : Click pour ingorer les cookies, revoir la classe")

    
    # Attendre la récupération des prix 
    def wait_contenance(self, driver):
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.configs[self.name]["contenance"]))
            )
        except:
            self.errors.append("Erreur étape : recherche par classe contenance, revoir la classe")
    
    # Sélection dynamique des prix pour Marionnaud
    def select_by_price(self, driver, step):
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, self.configs[self.name]['contenance'])
            elements[step].click()
            time.sleep(3)
        except:
            self.errors.append("Erreur étape (Marionnaud): click sur contenance, revoir la classe")

        
    # Sauvegarde des pages 
    def savehtml(self):
        url = self.url_input.split("?")[0]
        driver = self.config_driver()
        driver.get(url)

        # Séparer pour marionnaud du reste
        if self.name != "marionnaud":
            self.wait_contenance(driver)
            html_source = driver.page_source
            with open(self.file_output + "_" + self.now + ".html", "w", encoding="utf-8") as file:
                file.write(html_source)
        
        # Spécifique Marionnaud
        else:
            self.skip_cookies(driver)
            self.wait_contenance(driver)
            for i in list(range(0, 3)):
                self.select_by_price(driver, i)
                html_source = driver.page_source
                with open(self.file_output+"-price-v" + str(i) + "_" + self.now +".html", "w", encoding="utf-8") as file:
                    file.write(html_source)
        driver.quit()
        
        filename = self.file_output.split("/")
        if filename[2] not in os.listdir("scrapper/data/"):
            self.errors.append(f"Etape enregistrement du fichier {self.file_output+'.html'} : le fichier n'a pas été enregistré.")
        
        # Afficher le résultats si tout va bien
        print(f"{'---' * 3}")
        print(f"{self.name} is scrapped and saved in html file" if len(self.errors) < 1 else f"Erreur : \n{self.errors}")
        print(f"{'---' * 3}")

# # # # # # # # # #
# Step --> Parse  #
# # # # # # # # # #
class Parser:
    def __init__(self, file_output: str, name: str ,configs: dict):
        self.file_output = file_output
        self.name = name
        self.configs = configs
        self.now = datetime.now().strftime("%d-%m-%Y")
        self.errors = list()
        self.data = {"contenance": [], "prix": []}

    # Retrouver le html
    def retreive_html(self):
        try:
            with open(self.file_output + "_" + self.now + ".html") as file:
                content = file.read()
                soup = BeautifulSoup(content, "html.parser")
                return soup
        except FileNotFoundError:
            self.errors.append("Etape lecture fichier : Le fichier spécifié est introuvable.")
    
    # Récupérer les contenances
    def get_contenance(self):
        soup = self.retreive_html()
        contenance_elements = soup.select(self.configs[self.name]["contenance"])
        if not contenance_elements:
            self.errors.append("Etape extraction contenance : La classe contenant la contenance n'a pas été trouvée.")
        else:
            for e in contenance_elements:
                cleaned_text = e.text.replace("\n", "")
                cleaned_text = cleaned_text.strip()
                self.data["contenance"].append(cleaned_text)
   
    # Récupérer les prix
    def get_price(self):
        soup = self.retreive_html()
        prix_elements = soup.select(self.configs[self.name]["prix"])
        if not prix_elements:
            self.errors.append("Etape extraction prix : La classe contenant les prix n'a pas été trouvée.")
        else:
            for e in prix_elements:
                cleaned_text = e.text.replace(",", ".").replace("€", "").replace("\n", "").replace("(1)", "")
                cleaned_text = cleaned_text.strip()
                self.data["prix"].append(cleaned_text)
    
    # Enregistrer les données en json
    def save_json(self):
        self.retreive_html()
        self.get_contenance()
        self.get_price()
        
        with open(self.file_output + "_" + self.now +".json", "w") as json_file:
            json.dump(self.data, json_file, ensure_ascii=False, indent=4)
        
        filename = self.file_output.split("/")
        if filename[2] not in os.listdir("scrapper/data/"):
            self.errors.append(f"Etape enregistrement du fichier {self.file_output} : le fichier n'a pas été enregistré.")
        
        print(f"{'---' * 3}")
        print(f"{self.name} is scrapped in json file" if len(self.errors) < 1 else f"Erreur : \n{self.errors}")
        print(f"{'---' * 3}")
