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
        WebDriverWait(driver, 50).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "home-product-name")))
        WebDriverWait(driver, 50).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "originalPrice")))
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
    geral = {"Produto": namesList,
             "Preço Base": pricesList, "Preço Final": pricesList}
    df = pd.DataFrame(geral)
    f = "farid2.csv"
    df.to_csv(f, mode='a', header=not os.path.exists(f))


def main():
    service = Service(ChromeDriverManager().install())
    names = []
    prices = []
    namesList = []
    pricesList = []
    links = []
    linklist = []

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    #options.add_argument("user-data-dir=./chromeprofile")
    options.add_argument('--disable-extensions')
    options.add_argument("--disable-plugins-discovery")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.faridemcasa.com.br/pwa-app/")

    #pegando as tags a dentro das divs
    try:
        WebDriverWait(driver, 50).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'top-category-list')))
        div = driver.find_elements(By.CLASS_NAME, 'top-category-list')
        for d in div:
            links.append(d.find_element(By.TAG_NAME, 'a'))
    except:
        print('erro conection')
    
    #extraindo os links das tags
    for link in links:
        linklist.append(link.get_attribute('href'))
    
    #acessando links e pegando produtos
    for l in linklist:
        driver.get(l)
        try:
            WebDriverWait(driver, 50).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "home-product-name")))
            names = driver.find_elements(By.CLASS_NAME, "home-product-name")

            WebDriverWait(driver, 50).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "originalPrice")))
            prices = driver.find_elements(By.CLASS_NAME, "originalPrice")

            for n in names:
                namesList.append(n.text)

            for p in prices:
                pricesList.append((p.text))
        
        except:
            print('erro names and prices')
        
        time.sleep(t)

    driver.quit()
    for p in pricesList:
        p = re.sub(",", ".", p)
        p = re.sub("[^0-9,0-9]", '', p)
    
    criaCsv(namesList, pricesList)


if __name__ == "__main__":
    main()
