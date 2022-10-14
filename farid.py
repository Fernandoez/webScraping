from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import re

t = 5


def coleta(driver):

    try:
        WebDriverWait(driver, 50).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "home-product-name")))
        WebDriverWait(driver, 50).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "originalPrice")))
        names = driver.find_elements(By.CLASS_NAME, "home-product-name")
        prices = driver.find_elements(By.CLASS_NAME, "originalPrice")
        
    except:
        driver.quit()

    namesList = []
    pricesList = []

    for n in names:
        namesList.append((n.text))

    for p in prices:
        p = re.sub(",", '.', p)
        p = re.sub("[^0-9.0-9]", '', p)
        pricesList.append(float(p))

    return (namesList, pricesList)


def criaCsv(namesList, pricesList):
    geral = {"Produto": namesList,"Preço Base": pricesList, "Preço Final": pricesList}
    df = pd.DataFrame(geral)
    f = "farid2.csv"
    df.to_csv(f, mode='a', header=not os.path.exists(f))


def main():
    service = Service(ChromeDriverManager().install())
    names = []
    prices = []
    namesList = []
    pricesList = []


    driver = webdriver.Chrome(service=service)
    driver.get("https://www.faridemcasa.com.br/pwa-app/")
    time.sleep(t)
    
    # carnes
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'Carnes, aves e peixes'))).click()
        (names, prices) = coleta(driver)       
    except:
        driver.quit()
    
    namesList = namesList + names
    pricesList = pricesList + prices
    driver.back()
    time.sleep(t)

    # frios e laticinios
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'Frios e laticínios'))).click()
        (names, prices) = coleta(driver)
    except:
        driver.quit()

    namesList = namesList + names
    pricesList = pricesList + prices
    driver.back()
    time.sleep(t)

    # limpeza
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'Limpeza'))).click()
        (names, prices) = coleta(driver)
    except:
        driver.quit()

    namesList = namesList + names
    pricesList = pricesList + prices
    driver.back()
    time.sleep(t)

    # padaria
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'Salgadinhos'))).click()
        (names, prices) = coleta(driver)
    except:
        driver.quit()

    namesList = namesList + names
    pricesList = pricesList + prices
    driver.back()
    time.sleep(t)

    # mercearia
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'Mercearia'))).click()
        (names, prices) = coleta(driver)
    except:
        driver.quit()

    namesList = namesList + names
    pricesList = pricesList + prices
    driver.back()
    time.sleep(t)

    # hortifruti
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'Hortifruti'))).click()
        (names, prices) = coleta(driver)
    except:
        driver.quit()

    namesList = namesList + names
    pricesList = pricesList + prices

    driver.quit()
    criaCsv(namesList, pricesList)



if __name__ == "__main__":
    main()
