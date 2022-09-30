from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
t = 10

def main():
    service = Service(ChromeDriverManager().install())
    names = []
    prices = []
    namesList = []
    pricesList = []

    driver = webdriver.Chrome(service=service)
    driver.get("https://www.sitemercado.com.br/")
    driver.find_element(By.XPATH, '/html/body/app-root/app-cookie-notice/div/button').click()
    #digitar o cep
    driver.find_element(By.TAG_NAME, 'input').send_keys("35400000" + Keys.RETURN)
    time.sleep(t)
    #digitar o endereço
    driver.find_element(By.ID, 'streetAddress').send_keys("Rua João Fernandes Vieira")
    driver.find_element(By.ID, 'neighborhood').send_keys("Bauxita")
    driver.find_element(By.ID, 'numberAddress').send_keys("256")
    driver.find_element(By.XPATH, '/html/body/ngb-modal-window/div/div/app-filter-stores-modal/div/div/app-address-form/form/div[6]/button').click()
    time.sleep(t)
    #confirmar localização
    driver.find_element(By.XPATH, '/html/body/ngb-modal-window/div/div/app-filter-stores-modal/div/div/app-address-map/div/div/div[3]/button[2]').click()
    time.sleep(t)
    driver.find_element(By.XPATH, '/html/body/ngb-modal-window/div/div/app-filter-stores-modal/div/div/app-store-list/div/app-filter/div/div[1]/button[2]').click()
    mercados = driver.find_elements(By.CLASS_NAME, 'item ng-star-inserted')
    time.sleep(t)
    
    for mercado in mercados:
        mercado.click()
        time.sleep(t)
        '''
        time.sleep(t)
        mercado.find_element(By.CLASS_NAME, 'item-menu active').click()
        secoes = mercado.find_elements(By.CLASS_NAME, 'content')
        time.sleep(t)
        for secao in secoes:
            secao.click()
        '''    

    
if __name__ == "__main__":
    main()