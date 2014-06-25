#!/usr/bin/python

# Es posible crear listas al vuelo
lista_original=range(100)
print "Esta es la lista original",lista_original
nueva_lista=[i*i for i in lista_original]
print "Esta es una nueva listai de los cuadrados de la lista original",nueva_lista
nueva_lista=[i*i for i in lista_original if i%2==0]
print "Es posible filtrar algunos valores (pares) de la lista con un if",nueva_lista


