import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

def testeNgrams():
    t1 = "LINGUICA PIF PAF CALABRESA FINA 240G"
    t2 = "LINGUICA CALABRESA PIF PAF 240G"

    vect = CountVectorizer(analyzer = 'word', ngram_range= (1, 1)) 

    vocab = vect.fit([t1, t2])
    
    test = vect.fit_transform([t1, t2])
    test = test.toarray()
    print(test)
    print(vocab.vocabulary_)
    intersection_list = np.amin(test, axis = 0) # Intersecção
    sum = np.sum(intersection_list)
    count = np.sum(test[0]) # Texto base para comparação
    print(sum/count)

if __name__ == "__main__":
    testeNgrams()
