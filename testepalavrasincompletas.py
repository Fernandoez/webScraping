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


#Faz a limpeza e transforma em maiusculo
def clearString():
    
    tabela = 'tabelas/final.csv'
    df = pd.read_csv(tabela, index_col=0)
    listProducts = df['Produto'].tolist()
    
    for product in listProducts:
        product = unidecode(product.upper())
        if(re.search(r' , ', product) ):
            product = re.sub(r' , ',r', ', product)
            print(product)


if __name__ == "__main__":
    clearString()

'''

re.sub(r'K\.G',r'KG', product)
re.sub(r'M\.L',r'ML', product)
re.sub(r'\.',r'. ', product)
re.sub(r'FGO | FGO.',r'FRANGO', string)
re.sub(r'ADES.',r'ADESIVA', product)
re.sub(r'IOG.',r'IOGURTE', product)
re.sub(r'TRANSP.',r'TRASPARENTE', product)
re.sub(r'UNI.',r'UNIDADE', product)
re.sub(r'INSET.',r'INSETICIDA', product)
re.sub(r'ESC.',r'ESCOVA', product)
re.sub(r'CHOC.',r'CHOCOLATE', product)
re.sub(r'MAION.',r'MAIONESE', product)
re.sub(r'DESOD.',r'DESODORANTE', product)
re.sub(r'BOV.',r'BOVINA', product)
re.sub(r'SUIN.',r'SUINO', product)
re.sub(r'CONT.',r'CONTRA', product)
re.sub(r'FILEZ.',r'FILEZINHO', product)
re.sub(r'REQ.',r'REQUEIJAO', product)
re.sub(r'TRAD | TRAD.',r'TRADICIONAL', product)
re.sub(r'MARG.',r'MARGARINA', product)
re.sub(r'C/',r'COM ', product)
re.sub(r'P. PAF',r'PIF PAF', product)
re.sub(r'FAT.',r'FATIADO', product)

'''