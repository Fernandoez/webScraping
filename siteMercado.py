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
    prices = []
    namesList = []
    pricesList = []

    driver = webdriver.Chrome(service=service)
    driver.get("https://www.sitemercado.com.br/")
    driver.find_element(By.XPATH, '/html/body/app-root/app-cookie-notice/div/button').click()
    
    try:
        
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-cookie-notice/div/button')))
        element.click()

        #digitar o cep
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'input'))).send_keys("35400000" + Keys.RETURN)
        
        #digitar o endereço
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'streetAddress'))).send_keys("Rua João Fernandes Vieira")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'neighborhood'))).send_keys("Bauxita")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'numberAddress'))).send_keys("256")
    
    except:
        driver.quit()

    try:
        #confirmar insercao de dados
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'btnAdd')))
        element.click()

        #confirmar localização
        confirmLocation = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/ngb-modal-window/div/div/app-filter-stores-modal/div/div/app-address-map/div/div/div[3]/button[2]')))
        confirmLocation.click()
    except:
        driver.quit()

    try:
        #btn retirada
        retirada = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/ngb-modal-window/div/div/app-filter-stores-modal/div/div/app-store-list/div/app-filter/div/div[1]/button[2]')))
        retirada.click()

        mercadoList = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'item ng-star-inserted')))
        print(mercadoList)
    except:
        driver.quit()    
    time.sleep(t)
    mercadoList = driver.find_elements(By.CLASS_NAME, 'item ng-star-inserted')
    for m in mercadoList:
        print(m)
    '''
    mercadoList = driver.find_elements(By.CLASS_NAME, 'item ng-star-inserted')
    for m in mercadoList:
        print(m.text)
        #funcao para coleta de dados
        #m.close()
        #time.sleep(t)
    '''

    driver.quit()

    
if __name__ == "__main__":
    main()