import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
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


csvName = "final.csv"
qtdProdutosComparados = 6

def testeNgrams(t1, t2):
    #remove caracteres especiais
    t1 = re.sub(r'[,-./]|\sBD',r'', t1) 
    #remove o que estiver dentro de parenteses
    t1 = re.sub(r'(\s\(.*?\))',r'', t1)
    t2 = re.sub(r'[,-./]|\sBD',r'', t2)
    t2 = re.sub(r'(\s\(.*?\))',r'', t2)
    t2 = re.sub(r'FGO',r'FRANGO', t2)
    t2 = unidecode(t2.upper())
    print(t1)

    vect = CountVectorizer(analyzer = 'char', ngram_range= (2, 3)) 
    vocab = vect.fit([t1, t2])
    test = vocab.fit_transform([t1, t2])
    test = test.toarray()
    #print(vocab.vocabulary_)
    intersection_list = np.amin(test, axis = 0) # Intersecção
    #print(intersection_list)
    sum = np.sum(intersection_list)
    count = np.sum(test[0]) # Texto base para comparação
    print(sum/count)
    return (sum/count)


def consultaGtin():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://cosmos.bluesoft.com.br/")
    listGTIN = []
    listName = []
    captureName = []
    captureGtin = []
    nome = ''
    codigo = 0
    match = 0.0
    maxmatch = 0.0


    # Pegando a coluna com os nomes para a pesquisa
    df = pd.read_csv('farid.csv', index_col=0)
    listProducts = df['Produto'].tolist()

    #cookies
    driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/button').click()

    for product in listProducts:    
        try:
            
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'search-input')))
            element.clear()
            element.send_keys(product + Keys.RETURN)

            # lista com os nomes que estão no site
            captureName = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'item-title')))
            captureGtin = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="tbl-produtos"]/li/div[2]/ul/li[2]')))
            for i in range(qtdProdutosComparados):
                nome = captureName[i].find_element(By.TAG_NAME, 'a').get_attribute('text')
                codigo = captureGtin[i].find_element(By.TAG_NAME, 'a').get_attribute('text')
                match = testeNgrams(nome, product)
                if(match > maxmatch):
                    maxmatch = match
                    nomeFinal = re.sub(r'(\s\(.*?\))',r'', nome)
                    codigoFinal = codigo
            maxmatch = 0.0
            listName.append(nomeFinal)
            listGTIN.append(codigoFinal)
            break
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

if __name__ == "__main__":
    consultaGtin()


    
