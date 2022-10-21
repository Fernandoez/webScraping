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
from sklearn.feature_extraction.text import TfidfVectorizer
from sparse_dot_topn import awesome_cossim_topn

qtdProdutosComparados = 6

t1 = ['LINGUICA CALABRESA PIF PAF KG',
        'LINGUICA PIF PAF 240G JOSEFINA PCT.',
        'LINGUICA CALABRESA PIF PAF 240G',
        'LINGUICA PIF PAF',
        'LINGUIÇA MINEIRA PIF PAF',
        'LASANHA PIF PAF CALABRESA']
t2 = 'LINGUIÇA PIF PAF CALABRESA FINA 240G'

def testeNgrams(t1, t2):
    count_vectorizer = CountVectorizer()

    # Learn a vocabulary dictionary of all tokens in the raw documents.
    vocabulary = count_vectorizer.fit(t1 + [t2]).vocabulary_

    #print(vocabulary)

    tfidf_vectorizer = TfidfVectorizer(vocabulary=vocabulary)

    # Learn vocabulary and idf, return term-document matrix.
    tfidf_t2 = tfidf_vectorizer.fit_transform([t2])

    #print(tfidf_t2)

    tfidf_t1 = tfidf_vectorizer.fit_transform(t1).transpose()

    #print(tfidf_t1)

    results = awesome_cossim_topn(tfidf_t2, tfidf_t1, qtdProdutosComparados, 0)

    max = (results.argmax())
    '''
    print(t2)
    print('-------------------')

    for index, i in enumerate(results.indices):
        print('{}: {}'.format(t1[i], results.data[index]))
    '''
    return(t1[max])


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