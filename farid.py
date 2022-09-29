from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
t = 5

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
  df.to_csv(f, mode='a', header = not os.path.exists(f))


def main(): 
  service = Service(ChromeDriverManager().install())
  names = []
  prices = []
  namesList = []
  pricesList = []

  driver = webdriver.Chrome(service = service)
  driver.get("https://www.faridemcasa.com.br/pwa-app/")
  time.sleep(t)

  #carnes
  driver.find_element('xpath', '//*[@id="1008"]/img').click()
  time.sleep(t)
  (names, prices) = coleta(driver)
  namesList = namesList + names
  pricesList = pricesList + prices
  driver.back()
  time.sleep(t)

  #frios e laticinios
  driver.find_element('xpath', '//*[@id="1007"]/img').click()
  time.sleep(t)
  (names, prices) = coleta(driver)
  namesList = namesList + names
  pricesList = pricesList + prices
  driver.back()
  time.sleep(t)

  #limpeza
  driver.find_element('xpath', '//*[@id="1004"]/img').click()
  time.sleep(t)
  (names, prices) = coleta(driver)
  namesList = namesList + names
  pricesList = pricesList + prices
  driver.back()
  time.sleep(t)

  #padaria
  driver.find_element('xpath', '//*[@id="9150"]/img').click()
  time.sleep(t)
  (names, prices) = coleta(driver)
  namesList = namesList + names
  pricesList = pricesList + prices
  driver.back()
  time.sleep(t)

  #mercearia
  driver.find_element('xpath', '//*[@id="1002"]/img').click()
  time.sleep(t)
  (names, prices) = coleta(driver)
  namesList = namesList + names
  pricesList = pricesList + prices
  driver.back()
  time.sleep(t)

  #hortifruti
  driver.find_element('xpath', '//*[@id="1009"]/img').click()
  time.sleep(t)
  (names, prices) = coleta(driver)
  namesList = namesList + names
  pricesList = pricesList + prices

  criaCsv(namesList, pricesList)

  driver.quit()

if __name__ == "__main__":
  main()
