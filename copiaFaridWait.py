from pickletools import uint1
from xml.dom.minidom import Element
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def coleta(driver):
    names = driver.find_elements(By.CLASS_NAME, "home-product-name")
    prices = driver.find_elements(By.CLASS_NAME, "originalPrice")
    namesList = []
    pricesList = []

    for n in names:
        namesList.append((n.text))

    for p in prices:
        p = (p.text)[:-7]
        pricesList.append((p))

    return (namesList, pricesList)


def criaCsv(namesList, pricesList):
    geral = {"Produtos": namesList, "Precos": pricesList}
    df = pd.DataFrame(geral)
    f = "farid.csv"
    df.to_csv(f, mode='a', header=not os.path.exists(f))


def main():
    service = Service(ChromeDriverManager().install())
    names = []
    prices = []
    namesList = []
    pricesList = []

    driver = webdriver.Chrome(service=service)
    driver.get("https://www.faridemcasa.com.br/pwa-app/")
    #time.sleep(5)
    # carnes
    element = WebDriverWait(driver, timeout=10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="1008"]')))
    element.click()
    
    (names, prices) = coleta(driver)
    namesList = namesList + names
    pricesList = pricesList + prices
    driver.back()
    time.sleep(10)

if __name__ == "__main__":
    main()