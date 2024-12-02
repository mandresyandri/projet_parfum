import os
import re
import socket
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService

# Fonction 1 
def getstaticurl(i_url_str):
    return i_url_str.split("?")[0]

# Fonction 2
def isconnection():
    try:
        socket.create_connection(("https://www.wikipedia.org/", 80))
        return True
    except OSError:
        pass
    return False

# Fonction 3
def isurlvalid(i_url_str):
    # Source regex : https://stackoverflow.com/questions/3809401/what-is-a-good-regular-expression-to-match-a-url
    pattern_url = re.compile(r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})")
    return re.match(pattern_url, i_url_str) is not None

# Fonction 4
def gethtml(i_url_str):
    # Paramétrage de l'utilisation headless + paramètre utiles au driver
    # pour ne pas avoir d'erreur : https://stackoverflow.com/questions/67744514/timeout-exception-error-on-using-headless-chrome-webdriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        )
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Configuration de base --> URL + Driver
    url = "https://www.marionnaud.fr/nina-ricci/b/100520"
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options
    )

    # Premier éléments --> lancement du webdriver + étape ignorer les cookies éviter d'avoir les cookies
    driver.get(url)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div#onetrust-close-btn-container"))
    )

    # # Ignorer les cookies
    cookies = driver.find_element(By.CSS_SELECTOR, "div#onetrust-close-btn-container")
    cookies.click()

    # Exporter les données HTML
    html_source = driver.page_source
    
    # Fermer le driver
    driver.quit()
    
    return html_source
    

def savehtml(o_filename_str):
    # Paramétrage de l'utilisation headless + paramètre utiles au driver
    # pour ne pas avoir d'erreur : https://stackoverflow.com/questions/67744514/timeout-exception-error-on-using-headless-chrome-webdriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        )
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Configuration de base --> URL + Driver
    url = "https://www.marionnaud.fr/nina-ricci/b/100520"
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options
    )

    # Premier éléments --> lancement du webdriver + étape ignorer les cookies éviter d'avoir les cookies
    driver.get(url)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div#onetrust-close-btn-container"))
    )

    # # Ignorer les cookies
    cookies = driver.find_element(By.CSS_SELECTOR, "div#onetrust-close-btn-container")
    cookies.click()

    # Exporter les données HTML
    html_source = driver.page_source
    with open(o_filename_str, "w", encoding="utf-8") as file:
        file.write(html_source)

    # Fermer le driver
    driver.quit()

savehtml(o_filename_str)