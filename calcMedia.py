import pandas as pd

def calcMedia():
    df = pd.read_csv("testeMedia.csv", usecols=['Codigo_GTIN', 'Preço Final'])
    codigo = df['Codigo_GTIN'].tolist()
    valor = df['Preço Final'].tolist()
    codigoValor = []
    codigoValorQtd = {}
    
    #separando os codigos e os precoes referentes a eles
    for i in range(len(codigo)):
        codigoValor.append([codigo[i], valor[i]])
    #verificando cada codigo, se existir atualizo o dicionario com o valor que ele já possiu mais a soma do elemento atual
    #e acrescento 1 na quantidade. Caso não exista coloco o elemento no dicionário com o valor atual e inicializo a quantidade
    #para 1
    for elemento in codigoValor:
        if elemento[0] in codigoValorQtd:
            el = (elemento[0])
            soma = elemento[1] + codigoValorQtd.get(el)[0]
            qtd = codigoValorQtd.get(el)[1] + 1
            media = soma/qtd
            codigoValorQtd.update({el: (soma, qtd, media)})
        else:
            codigoValorQtd.update({elemento[0]: (elemento[1], 1, elemento[1])})
    print(codigoValorQtd)
    tabela = {"Código": namesList,
             "Preço Base": pricesList, "Preço Final": pricesList}


if __name__ == "__main__":
    calcMedia()