import pandas as pd
import re
import unidecode
import itertools

emoji_dict_SEA = pd.read_excel('webapp/data/DiccionarioEmojisconEmojisAdelante.xlsx')
jergas_defs = pd.read_excel('webapp/data/Diccionario Jergas Peruanas.xlsx')

with open('webapp/data/stopwords_f1.txt') as f:
    stopwords_f1 = f.read().splitlines()

def cleanSentence(sen):
    t = sen[:]
    t = t.lower()

    t = unidecode.unidecode(t) 
    t = re.sub(r'\([^)]*\)', '', t)
    t = re.sub(u'[^a-zA-ZáéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇñ@# ]', '', t)
    return t

def replaceJergas(comment):
    comment_temp = comment[:]
    for index,row in jergas_defs.iterrows():

        temp = cleanSentence(row['Jerga'])
        old = temp[:]

        for word in temp.split(' '):
            newword = ''.join(ch for ch, _ in itertools.groupby(word))
            temp = temp.replace(word, newword)

        comment_temp = re.sub(r'\b'+temp+r'\b', cleanSentence(row['Significado']), comment_temp)

    return comment_temp

def busqueda_binaria(arreglo, busqueda):
    izquierda, derecha = 0, len(arreglo) - 1
    while izquierda <= derecha:
        indiceDelElementoDelMedio = (izquierda + derecha) // 2
        elementoDelMedio = arreglo[indiceDelElementoDelMedio]
        if elementoDelMedio == busqueda:
            return indiceDelElementoDelMedio
        if busqueda < elementoDelMedio:
            derecha = indiceDelElementoDelMedio - 1
        else:
            izquierda = indiceDelElementoDelMedio + 1
    # Si salimos del ciclo significa que no existe el valor
    return -1

def preprocesamiento(X):
    unis = ['upc','pucp','cato','ucv','unmsm','upn','uni']
    # SE PUEDE MEJORAR El PREPROCESAMIENTO

    #Eliminar [] mal extraídos
    list_word = []
    for word in X.split():
        if not (word[0] == '[' and word[len(word)-1] == "]"):
            word = word.replace("[","").replace("]","")
        list_word.append(word)
    X= " ".join(list(list_word))
    del(list_word)

    #emojis
    for index2, row2 in emoji_dict_SEA.iterrows():
        X = X.replace(row2[1]," " + row2[2]+" "+' ')

    #Hacer minuscula
    X = X.lower()
        
    #Sacar urls - \S es para cualquier caracter que no es un whitespace
    X = re.sub(r"http\S+", "", X)

    # #Sacar caracteres duplicados
    for word in X.split(' '):
        if(not ('ll' in word[1:-1]) or not ('rr' in word[1:-1])):
            newword = ''.join(ch for ch, _ in itertools.groupby(word))
            X = X.replace(word, newword)

    #Reemplazar mentions FB con [Persona]
    X = re.sub(r'\[(.*?)\]','personaTag', X)
    
    #Sacar hashtags
    X = re.sub(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))#([A-Za-z]+[A-Za-z0-9-_]+)','', X)

    #sacar acentos
    X = unidecode.unidecode(X) 

    #Arreglar 'io' por yo
    X = re.sub(r"\bio" ,'yo', X)
    
    #Sacar line breaks
    X.replace(r'\r', ' ')
    X.replace(r'\n', ' ')
        
    #Remplazar cada manera de la palabra "jajajaja" a "jaja" - Esto toma en cuenta la existencia de ja también? O no depende del orden?
    for word in X.split(' '):
        if (all(c in "aj" for c in word)) or (all(c in "ah" for c in word) ):
            X = X.replace(word, '')
        
    #Sin caracteres especiales
    X= re.sub(u'[^a-zA-ZáéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇñ@# ]', '', X)
    
    #Arreglo espacios innecesarios
    X = re.sub(' +', ' ', X)

    #Reemplazar el keyword de un mention por [PERSONA]
    X = X.replace('personaTag','[PERSONA]')

    #if(reJergas):
    X = replaceJergas(X)

    for univ in unis:
        X = re.sub(r'\b'+univ+r'\b', '[UNIVERSIDAD] ', X)
        X = re.sub(r''+univ+r'\b', '[UNIVERSIDAD] ', X)

    #Quitar stopwords segun caso
    X= " ".join([word for word in X.split() if busqueda_binaria(stopwords_f1,word.lower())==-1])
    return X