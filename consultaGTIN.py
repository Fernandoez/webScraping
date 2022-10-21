from operator import index
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import datetime
import re
from unidecode import unidecode
import os
import glob


csvName = "final.csv"

#Junta todos os documentos em um únigo dataframe
def concatDtFrames():
    os.chdir("./")
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    #combinar todos os arquivos da lista
    combined_csv = pd.concat([pd.read_csv(f, index_col=0) for f in all_filenames ], ignore_index=True)
    #exportar para csv
    combined_csv.to_csv( csvName, encoding='utf-8-sig')


#Remove ponto, Ç, acentuação e transforma em caixa alta
def stringCorrection():
    df = pd.read_csv(csvName, index_col=0)
    productList = df['Produto'].to_list()
    newProductList = []
    for p in productList:
        
        p = re.sub("['|-]", '', p)
        p = re.sub("[ç]", 'c', p)
        newProductList.append(unidecode(p.upper()))

    df['Produto'] = newProductList
    df.to_csv(csvName)

def consultaGtin():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://cosmos.bluesoft.com.br/")
    listGTIN = []
    listName = []

    # Pegando a coluna com os nomes para a pesquisa
    df = pd.read_csv(csvName, index_col=0)
    listProducts = df['Produto'].tolist()

    #cookies
    driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/button').click()

    for product in listProducts:    
        try:
            
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'search-input')))
            element.clear()
            element.send_keys(product + Keys.RETURN)

            # lista com os nomes que estão no site
            captureName = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tbl-produtos"]/li[1]/div[2]/h5/a')))
            listName.append(captureName.text)

            # lista com os códigos que estão no site
            capturaGtin = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tbl-produtos"]/li[1]/div[2]/ul/li[2]/a')))
            listGTIN.append(capturaGtin.text)
        
        except:
            driver.quit()
    driver.quit()
    
    #pegando a data da geracao do arquivo
    date = datetime.date.today()
    # Inserindo novo nome e codigos e gerando o dataframe final
    df['Produto'] = listName
    df['Codigo_GTIN'] = listGTIN
    df[date] = ""
    df.to_csv('final.csv')


def main(): 
    
    #funcao para transformar em uma tabela
    concatDtFrames()

    #funcao para padronizar as descricoes
    stringCorrection()

    #funcao para pegar os codigos no bluesoft
    consultaGtin()


if __name__ == "__main__":
    concatDtFrames()