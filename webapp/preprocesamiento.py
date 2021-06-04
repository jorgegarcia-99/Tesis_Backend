import pandas as pd
import nltk
import re
import unidecode
import itertools
from nltk.corpus import stopwords

stop = stopwords.words('spanish')
stopEnglish =stopwords.words('english')
emoji_dict = pd.read_excel('webapp/data/DiccionarioEmojisTildes.xlsx')

def preprocesamiento(X):
    unis = ['upc','pucp','cato','ucv','unmsm','upn','uni']
    x_temp  = [X] #tal vez no se usa
          
    #Hacer minuscula
    X = X.lower()
    #Eliminar [] mal extraídos
    list_word = []
    for word in X.split():
        if not (word[0] == '[' and word[len(word)-1] == "]"):
            word = word.replace("[","").replace("]","")
        list_word.append(word)
    X= " ".join(list(list_word))
    del(list_word)
    #Reemplazar mentions FB con [Persona]
    X = re.sub(r'\[(.*?)\]','personaTag', X)
    #Sin caracteres especiales
    X= re.sub(u'^a-zA-ZáéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇñ@# ', '', X)
    #Sacar urls
    X = re.sub(r"http\S+", "", X)
    #Sacar hashtags
    X = re.sub(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))#([A-Za-z]+[A-Za-z0-9-_]+)','', X)
    #Sacar caracteres duplicados
    for word in X.split(' '):
        newword = ''.join(ch for ch, _ in itertools.groupby(word))
        X = X.replace(word, newword)
    #Reemplazar mentions con [Persona]
    X = re.sub(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9-_.]+)','personaTag', X)
    #Reemplazar EMOJIS
    for index2, row2 in emoji_dict.iterrows():
        X = X.replace(row2[1],row2[4]+' ')
    #sacar acentos
    X = unidecode.unidecode(X) 
    #Arreglar 'io' por yo
    X = re.sub(r"\bio" ,'yo', X)
    #Quitar stopwords en Spanish y English
    X= " ".join([word for word in X.split() if word.lower() not in stop])
    X= " ".join([word for word in X.split() if word.lower() not in stopEnglish])       
    #Sacar line breaks
    X.replace(r'\r', ' ')
    X.replace(r'\n', ' ')       
    #Remplazar cada manera de la palabra "jajajaja" a "jaja" 
    for word in X.split(' '):
        if (all(c in "aj" for c in word)) or (all(c in "ah" for c in word)):
            X = X.replace(word, 'jaja')       
    #Remplazar cada manera de la palabra "xdxd" a "xd" 
    # for word in X.split(' '):
    #   if all(c in "xd" for c in word):
    #      X = X.replace(word, 'xd')
    #   elif all(c in "oe" for c in word):
    #      X = X.replace(word, 'oye')

    #Arreglo espacios innecesarios
    X = re.sub(' +', ' ', X)       
    #Reemplazar el keyword de un mention por [PERSONA]
    X = X.replace('personaTag','[PERSONA]')       
    #Quitar stopwords en spanish y english una vez mas
    X= " ".join([word for word in X.split() if word.lower() not in stop])
    X= " ".join([word for word in X.split() if word.lower() not in stopEnglish])
    return X