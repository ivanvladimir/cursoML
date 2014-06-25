#!/usr/bin/python
# -*- coding: utf-8 -*-

lista=['hola','mundo']
print "Iterando listas"
for w in lista:
    print "Este es un elemento de la lista",w

lista=range(10)
print "Iterando una lista dinámica",lista
for i in lista:
    print "Contando...",i


tupla=(1,2,3)
print "Iterando una tupla",tupla
for i in tupla:
    print i

diccionario={"hola":1,"mundo":2}
print "Iterando la listas de lementos de un diccionario",diccionario
for k,v in diccionario.items():
    print "Llave:",i
    print "Valor:",v

print "Iterando el diccionario directamente",diccionario
for k,v in diccionario.iteritems():
    print "Llave:",i
    print "Valor:",v


print "Un ciclo con while"
i=0
while i<10:
    print "Contanndo con while...",i
    i+=1

print "Rompiendo el ciclo"
i=0
while True:
    print "Contanndo con while...",i
    if i==10:
        break
    i+=1

print "lo que sigue es un ciclo infinito, teclea ctr+c para parar el programa"
while True:
    pass #Esta instrucción no hace nada


    




