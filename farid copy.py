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
        pricesList.append((p))

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
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/div/mat-sidenav-container/mat-sidenav-content/app-home/div[1]/div[1]/div/app-top-category/div/div/div/div')))
        links = element.find_elements(By.TAG_NAME, 'a')
        time.sleep(t)
        print(links)
        for link in links:
            link.click()
            time.sleep(t)
            (names, prices) = coleta(driver)       
    except:
        driver.quit()
    
    namesList = namesList + names
    pricesList = pricesList + prices
    driver.back()
    time.sleep(t)


    driver.quit()
    criaCsv(namesList, pricesList)



if __name__ == "__main__":
    main()
