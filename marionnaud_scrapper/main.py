import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService

# Paramétrage de l'utilisation headless --> 
# pour ne pas avoir d'erreur : https://stackoverflow.com/questions/67744514/timeout-exception-error-on-using-headless-chrome-webdriver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    )

# Configuration de base --> URL + Driver
url = "https://www.marionnaud.fr/nina-ricci/b/100520"
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=chrome_options
)

# Premier éléments --> lancement du webdriver + étape ignorer les cookies
driver.get(url)
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div#onetrust-close-btn-container"))
)

# # Ignorer les cookies
cookies = driver.find_element(By.CSS_SELECTOR, "div#onetrust-close-btn-container")
cookies.click()

# Function de collecte des données
def scrape_data(driver, selector):
    # Vérification présence de l'élément
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )

    # Récupération des données dans une liste
    data_array = list()
    for element in driver.find_elements(By.CSS_SELECTOR, selector):
        if len(element.text) > 0:
            data_array.append(element.text)

    return data_array

# Fermer le webdriver
driver.quit()

# Récupération des datas
nom = scrape_data(driver, "div.product-list-item__brand")
nom_spec = scrape_data(driver, "div.product-list-item__range")
type_prod = scrape_data(driver, "div.product-list-item__name")
price = scrape_data(driver, "span.price__current")

# Exporter en CSV
data = {
    "Nom": nom,
    "Nom_spec": nom_spec,
    "Type_prod": type_prod,
    "Price": price
}

df = pd.DataFrame(data)
df["site web"] = "Marionnaud"
df.to_csv("data/output.csv", index=False)

