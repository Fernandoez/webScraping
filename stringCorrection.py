import pandas as pd
import re

def stringCorrection():
    df = pd.read_csv('farid.csv', index_col=0)
    productList = df['Produto'].to_list()
    for p in productList:
        if(re.search("['|-]", p)):
            print(p)
        if(re.search("[ç]", p)):
            print(p)
        if(re.search("\. | ,", p)):
            print(p)

            
if __name__ == "__main__":
    stringCorrection()