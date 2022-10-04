from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
csvName = "teste.csv"

def concatDtFrames():
    df = pd.read_csv(csvName, index_col=0)
    print(df)


def removeCaracters():
    df = pd.read_csv(csvName, index_col=0)
    pricesList = df['Precos'].tolist()
    newPricesList = []
    carcaters = "R$"
    for p in pricesList:
        p = p.replace(carcaters, "")
        p = p.replace(',', '.')
        newPricesList.append(float(p))
    df['Precos'] = newPricesList
    df.to_csv(csvName)


def main(): 
    
    #funcao para transformar em uma tabela
    concatDtFrames()

    #funcao para remover os caracteres e transformar em numeros
    removeCaracters()

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://cosmos.bluesoft.com.br/")
    listGTIN = []
    listName = []

    # Pegando a coluna com os nomes para a pesquisa
    df = pd.read_csv(csvName, index_col=0)
    listProducts = df['Produtos'].tolist()

    #cookies
    driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/button').click()

    for product in listProducts:    
        try:
            
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'search-input')))
            element.clear()
            element.send_keys(product + Keys.RETURN)

            # lista com os nomes que estão no site
            capturaName = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tbl-produtos"]/li[1]/div[2]/h5/a')))
            listName.append(capturaName.text)

            # lista com os códigos que estão no site
            capturaGtin = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tbl-produtos"]/li[1]/div[2]/ul/li[2]/a')))
            listGTIN.append(capturaGtin.text)
        
        except:
            driver.quit()

    # Inserindo novo nome e codigos e gerando o dataframe final
    df['Produtos'] = listName
    df['Codigo_GTIN'] = listGTIN
    df.to_csv('teste.csv')


if __name__ == "__main__":
    concatDtFrames()