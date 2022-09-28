from lib2to3.pgen2 import driver
from os import link
from unicodedata import name
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
#import para ter acesso as Keys para maniupulação no site
from selenium.webdriver.common.keys import Keys
import time

#código padrão para sempre manter atualizado o webdriver
#necessário baixar o webdriver manager (pip install webdriver-manager)
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service = service)


driver.get("https://www.epa.com.br/")
time.sleep(5)
#cokkies
driver.find_element('xpath', '//*[@id="adopt-accept-all-button"]').click()
#bh e regiao
driver.find_element('xpath', '/html/body/main/section[2]/div/div/div/button[1]').click()
print(driver)
#baixar folheto de ofertas
driver.find_element('xpath', '/html/body/main/section[2]/div/div[3]/div/a').click()
time.sleep(5)
#baixar folheto
driver.find_element('xpath', '/html/body/main/section[3]/div/div[3]/a').click()

time.sleep(5)









'''
driver.get("https://www.google.com/")
print(driver.title)

#atribuinfo o elemento que possui o nome s na variável search
search = driver.find_element(By.NAME, "q")
#após encontrar o elemento, fazendo um input para pesquisar test
search.send_keys("test")
#usando comando para simular aperto da tecla enter
search.send_keys(Keys.RETURN)

time.sleep(5)


#comando para fechar a aba atual
#driver.close()
#comando para fechar o browser completo
driver.quit()

parte que seria usada no beautifulsoup
simular uma pessoa navegando para poder acessar determinados sites
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}

url = requests.get(driver.current_url, headers=headers)
doc = BeautifulSoup(tag, "html.parser")
'''