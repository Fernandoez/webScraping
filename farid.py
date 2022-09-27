from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os

def coleta(driver):
    names = driver.find_elements(By.CLASS_NAME, "home-product-name")
    prices = driver.find_elements(By.CLASS_NAME, "originalPrice")
    namesList = []
    pricesList = []

    for n in names:
      namesList.append((n.text))

    for p in prices:
      pricesList.append((p.text))

    geral = {"Produtos": namesList, "Precos": pricesList}
    df = pd.DataFrame(geral)
    f = "farid.csv"
    df.to_csv(f, mode='a', header = not os.path.exists(f))
    
    

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service = service)
driver.get("https://www.faridemcasa.com.br/pwa-app/")
time.sleep(10)
#carnes
driver.find_element('xpath', '//*[@id="1008"]/img').click()
time.sleep(10)
coleta(driver)
driver.back()
time.sleep(10)
#frios e laticinios
driver.find_element('xpath', '//*[@id="1007"]/img').click()
time.sleep(10)
coleta(driver)
driver.back()
time.sleep(10)
#limpeza
driver.find_element('xpath', '//*[@id="1004"]/img').click()
time.sleep(10)
coleta(driver)
driver.back()
time.sleep(10)
#padaria
driver.find_element('xpath', '//*[@id="9150"]/img').click()
time.sleep(10)
coleta(driver)
driver.back()
time.sleep(10)
#mercearia
driver.find_element('xpath', '//*[@id="1002"]/img').click()
time.sleep(10)
coleta(driver)
driver.back()
time.sleep(10)
#hortifruti
driver.find_element('xpath', '//*[@id="1009"]/img').click()
time.sleep(10)
coleta(driver)
time.sleep(10)
driver.quit()

'''
parte que seria usada no beautifulsoup
simular uma pessoa navegando para poder acessar determinados sites
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}

url = requests.get(driver.current_url, headers=headers)
doc = BeautifulSoup(tag, "html.parser")
'''