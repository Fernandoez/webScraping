from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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
import threading

#nome do arquivo final com todos os produtos
csvName = "teste.csv"
#quantidade de produtos da pagina que vamos pegar para comparar as descricoes
qtdProdutosComparados = 11


#Junta todos os documentos em um únigo dataframe
def concatDtFrames():
    os.chdir("./tabelas")
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    #combinar todos os arquivos da lista
    combined_csv = pd.concat([pd.read_csv(f, index_col=0) for f in all_filenames ], ignore_index=True)
    #exportar para csv
    combined_csv.to_csv( csvName, encoding='utf-8-sig')


#Faz a limpeza e transforma em maiusculo
def clearString(string):
    #remove caracteres especiais
    #newString = re.sub(r'[,-./]|\sBD',r'', string) 
    #remove o que estiver dentro de parenteses
    newString = re.sub(r'(\s\(.*?\))',r'', string)
    #transformando em maiúscula
    newString = unidecode(string.upper())
    
    newString = re.sub(r' - ',r' ', newString)
    newString = re.sub(r' , ',r', ', newString)
    newString = re.sub(r'K\.G',r'KG', newString)
    newString = re.sub(r'M\.L',r'ML', newString)
    if(re.search(r'[A-Z]+- ', newString) ):
        newString = re.sub(r'-',r'', newString)
    if(re.search(r'[A-Z]+\.[A-Z]+', newString) ):
        newString = re.sub(r'\.',r'. ', newString)
    newString = re.sub(r'KHAPPY',r'K-HAPPY', newString)
    newString = re.sub(r'FGO | FGO\.',r'FRANGO', newString)
    newString = re.sub(r'ADES\.',r'ADESIVA', newString)
    newString = re.sub(r'IOG\.',r'IOGURTE', newString)
    newString = re.sub(r'TRANSP\.',r'TRASPARENTE', newString)
    newString = re.sub(r'UNI\.',r'UNIDADE', newString)
    newString = re.sub(r'INSET\.',r'INSETICIDA', newString)
    newString = re.sub(r'ESC\.',r'ESCOVA', newString)
    newString = re.sub(r'CHOC\.',r'CHOCOLATE', newString)
    newString = re.sub(r'MAION\.',r'MAIONESE', newString)
    newString = re.sub(r'DESOD\.',r'DESODORANTE', newString)
    newString = re.sub(r'BOV\.',r'BOVINA', newString)
    newString = re.sub(r'SUIN\.',r'SUINO', newString)
    newString = re.sub(r'CONT\.',r'CONTRA', newString)
    newString = re.sub(r'FILEZ\.',r'FILEZINHO', newString)
    newString = re.sub(r'REQ\.',r'REQUEIJAO', newString)
    newString = re.sub(r'TRAD\.',r'TRADICIONAL', newString)
    newString = re.sub(r'MARG\.',r'MARGARINA', newString)
    newString = re.sub(r'DESINF\.',r'DESINFETANTE', newString)
    newString = re.sub(r'C/',r'COM ', newString)
    newString = re.sub(r'S/',r'SEM ', newString)
    newString = re.sub(r'P\. PAF',r'PIF PAF', newString)
    newString = re.sub(r'FAT\.',r'FATIADO', newString)
    newString = re.sub(r'LIMP\.',r'LIMPADOR', newString)

    return newString


#comparacao entre a descricao atual pega no site e o produto do nosso banco
def nGrams(t1, t2):
    vect = CountVectorizer(analyzer = 'char', ngram_range= (2, 3)) 
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
def consultGtin(listProducts):
    service = Service(ChromeDriverManager().install())
    
    options = Options()
    options.headless = True
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

    #cookies
    driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/button').click()
    for product in listProducts:    
        try:

            element = WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.ID, 'search-input')))
            element.clear()
            product = clearString(product)
            print(product)
            element.send_keys(product + Keys.RETURN)

            #lista com os nomes que estão no site
            captureName = WebDriverWait(driver, 200).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'item-title')))
            #lista com os cosigos de cada produto
            captureGtin = WebDriverWait(driver, 200).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="tbl-produtos"]/li/div[2]/ul/li[2]')))
            
            #caso a lista de itens seja menor do que o definido no incio
            if(len(captureName)<qtdProdutosComparados):
                comparacoes = len(captureName)
            else:
                comparacoes = qtdProdutosComparados
            
            #fazendo a comparacao com cada descricao
            for i in range(comparacoes):
                try:
                    nome = captureName[i].find_element(By.TAG_NAME, 'a').get_attribute('text')
                    codigo = captureGtin[i].find_element(By.TAG_NAME, 'a').get_attribute('text')
                    #match recebe o equivalente a porcentagem de igualdade, se for maior que as outras encontradas passamos a usar essa como a padrão
                    #e atribuímos ela ao nosso BD junto com o código
                except:
                    nomeFinal = product
                    codigoFinal = "0"
                if(codigo != "0"):
                    nome = clearString(nome)
                    print(product)
                    print(nome)
                    match = nGrams(nome, product)
                    if(match > maxmatch):
                        maxmatch = match
                        nomeFinal = nome
                        codigoFinal = codigo
            maxmatch = 0.0
            listName.append(nomeFinal)
            listGTIN.append(codigoFinal)
            print(nomeFinal)
            print(codigoFinal)
        except:
            print("Erro na pesquisa do produto: " + product)
            listName.append(product)
            listGTIN.append("0")
    driver.quit()
    
    return(listName, listGTIN)


def separaLista(listaCompleta, inicio, fim):
    listaSeparada = []
    for i in range(inicio, fim):
        listaSeparada.append(listaCompleta[i])
    return listaSeparada

def main(): 
    #funcao para transformar em uma tabela
    #concatDtFrames()

    # Pegando a coluna com os nomes para a pesquisa
    df = pd.read_csv(csvName, index_col=0)
    listProducts = df['Produto'].tolist()
    n = int (len(listProducts) / 4)
    
    #separando os blocos de listas
    listProducts1 = separaLista(listProducts, 0, n)
    listProducts2 = separaLista(listProducts, n+1, n*2)
    listProducts3 = separaLista(listProducts, n*2+1, n*3)
    listProducts4 = separaLista(listProducts, n*3+1, len(listProducts))

    #funcao para pegar os codigos no bluesoft com threads
    (listName1, listGTIN1) = threading.Thread(target=consultGtin(listProducts1)) 
    (listName2, listGTIN2) = threading.Thread(target=consultGtin(listProducts2)) 
    (listName3, listGTIN3) = threading.Thread(target=consultGtin(listProducts3)) 
    (listName4, listGTIN4) = threading.Thread(target=consultGtin(listProducts4))

    #juntando as listas modificadas
    listName = listName1 + listName2 + listName3 + listName4
    listGTIN = listGTIN1 + listGTIN2 + listGTIN3 + listGTIN4

    #pegando a data da geracao do arquivo
    date = datetime.date.today()
    # Inserindo novo nome e codigos e gerando o dataframe final
    df['Produto'] = listName
    df['Codigo_GTIN'] = listGTIN
    df[date] = ""
    df.to_csv(csvName)


if __name__ == "__main__":
    inicio = datetime.datetime.now()
    main()
    print(inicio)
    print(datetime.datetime.now())