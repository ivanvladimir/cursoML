# Cargando librerias
from __future__ import division  # Python 2 users only
import nltk, re, pprint
from nltk import word_tokenize

# Cargando archivos
raw = open('pg2000.txt').read().decode('utf8')
print type(raw)
print len(raw)

# Tokens
tokens = word_tokenize(raw)
print type(tokens)
print len(tokens)
print tokens[:10]

# Texto
text = nltk.Text(tokens)
print type(text)
print text[1000:1020]


# Estadisticas basicas
print len(set(text))
print text.count('Sancho')
fd = nltk.FreqDist(text)
print fd['Dulcinea']
print fd.keys()[0:50]
print fd.plot(50,cumulative=False)
lengths= [len(w) for w in text]
fd2= nltk.FreqDist(lengths)
fd2.tabulate()

# Colocaciones
print text.collocations()

# Ngramas
from nltk.util import ngrams
bigrams = ngrams(text, 2)
fd3= nltk.FreqDist(bigrams)                                                      
trigrams = ngrams(text, 3)
fd4= nltk.FreqDist(trigrams)                                                      
sixgrams = ngrams(text, 6)
fd5= nltk.FreqDist(sixgrams)
print fd3.most_common(20)
print fd4.most_common(20)
print fd5.most_common(20)
