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
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

#nome do arquivo final com todos os produtos
csvName = "final.csv"
#quantidade de produtos da pagina que vamos pegar para comparar as descricoes
qtdProdutosComparados = 5


#Junta todos os documentos em um únigo dataframe
def concatDtFrames():
    os.chdir("./")
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    #combinar todos os arquivos da lista
    combined_csv = pd.concat([pd.read_csv(f, index_col=0) for f in all_filenames ], ignore_index=True)
    #exportar para csv
    combined_csv.to_csv( csvName, encoding='utf-8-sig')


#Faz a limpeza e transforma em maiusculo
def clearString(string):
    #remove caracteres especiais
    newString = re.sub(r'[,-./]|\sBD',r'', string) 
    #remove o que estiver dentro de parenteses
    newString = re.sub(r'(\s\(.*?\))',r'', string)
    #substituindo FGO por FRANGO
    newString = re.sub(r'FGO',r'FRANGO', string)
    #transformando em maiúscula
    newString = unidecode(string.upper())
    return newString


#comparacao entre a descricao atual pega no site e o produto do nosso banco
def nGrams(t1, t2):
    vect = CountVectorizer(analyzer = 'char', ngram_range= (1, 2)) 
    vocab = vect.fit([t1, t2])
    test = vocab.fit_transform([t1, t2])
    test = test.toarray()
    #print(vocab.vocabulary_)
    intersection_list = np.amin(test, axis = 0) # Intersecção
    #print(intersection_list)
    sum = np.sum(intersection_list)
    count = np.sum(test[0]) # Texto base para comparação
    #print(sum/count)
    return (sum/count)


#realiza a pesquisa no site BlueSoft usando a descricao do nosso banco
def consultGtin():
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
    df = pd.read_csv(csvName, index_col=0)
    listProducts = df['Produto'].tolist()

    #cookies
    driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/button').click()

    for product in listProducts:    
        try:
            
            element = WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.ID, 'search-input')))
            element.clear()
            product = clearString(product)
            element.send_keys(product + Keys.RETURN)

            #lista com os nomes que estão no site
            captureName = WebDriverWait(driver, 200).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'item-title')))
            #lista com os cosigos de cada produto
            captureGtin = WebDriverWait(driver, 200).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="tbl-produtos"]/li/div[2]/ul/li[2]')))
            #fazendo a compracao com cada descricao
            for i in range(qtdProdutosComparados):
                nome = captureName[i].find_element(By.TAG_NAME, 'a').get_attribute('text')
                codigo = captureGtin[i].find_element(By.TAG_NAME, 'a').get_attribute('text')
                #match recebe o equivalente a porcentagem de igualdade, se for maior que as outras encontradas passamos a usar essa como a padrão
                #e atribuímos ela ao nosso BD junto com o código
                nome = clearString(nome)
                match = nGrams(nome, product)
                if(match > maxmatch):
                    maxmatch = match
                    nomeFinal = nome
                    codigoFinal = codigo
            maxmatch = 0.0
            listName.append(nomeFinal)
            listGTIN.append(codigoFinal)

        except:
            driver.quit()
    driver.quit()
    
    #pegando a data da geracao do arquivo
    date = datetime.date.today()
    # Inserindo novo nome e codigos e gerando o dataframe final
    df['Produto'] = listName
    df['Codigo_GTIN'] = listGTIN
    df[date] = ""
    df.to_csv(csvName)


def main(): 
    
    #funcao para transformar em uma tabela
    concatDtFrames()

    #funcao para pegar os codigos no bluesoft
    consultGtin()


if __name__ == "__main__":
    main()