#!/usr/bin/python

# Esto es un comentario
print "Esto es una cadena con comillas dobles"
print 'Esto es otra cadena con comillas simples'


print "Esto es un booleano verdadero",True
print "Esto es un booleano false",False

print "Esto es un entero",123
print "Esto es un flotante",123.456

variable=5
print "Esto es un variable",variable
print "Esta es la variable más uno", variable+1

variable="hola"
print "Esta es la misma variable per con otro valor",variable
print "También pordemos 'sumar' dos cadenas", variable+" mundo"

lista=[1,2,3]
print "Esta es una variable asociada a una lista",lista
print "Este es el primer valor de la lista",lista[0]
print "Este es el último valor de la lista",lista[-1]
print "Estos son los dos primeros valores",lista[0:1]
print "Esta es la longitud de la lista",len(lista)

lista=["hola",1,"mundo"]
print "Esta una lista con valores de diferente tipos",lista
lista.append('!')
print "Esta es la misma lista con un valo extra",lista
lista[1]=','
print "Esta es la misma lista con el segundo valor cambiado",lista


tupla=(1,2,3)
print "Esta es una tupla",tupla
print "Este es el primer valor de la tupla",tupla[0]
print "Este es el último valor de la tupla",tupla[-1]
print "Estos son los dos primeros valores",tupla[0:1]
print "Esta es la longitud de la lista",len(tupla)
print "La tupla no se puede aumentar o cambiar"

diccionario={"hola":1,"mundo":2}
print "Este es un diccionario", diccionario
print "Este es un elemento del diccionario",diccionario['mundo']
print "Este es otro elemento del diccionario",diccionario['hola']
print "Estas son las llaves del diccionario",diccionario.keys()
print "Estos son los valores del diccionario",diccionario.values()
print "Estos son los elementos del diccionario",diccionario.items()

rara=[({'hola':1,"mundo":2},"hola mundo"),["hola","mundo"]]
print "Este es una estructura rara",rara




