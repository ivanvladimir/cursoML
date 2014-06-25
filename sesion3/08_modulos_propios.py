#!/usr/bin/python

import mimodulo

print "El porcentage de 0.1 es"
mimodulo.print_percentage(0.1)

print "El porcentage de 0.02 es"
mimodulo.print_percentage(0.02)

lista=range(20)
print "La suma de la lista",lista,"es",mimodulo.suma_lista(lista)
lista=range(200)
print "La suma de la lista",lista,"es",mimodulo.suma_lista(lista)

lista=range(20)
print "El número de fibonacci para 10 es",mimodulo.fib(10)
lista=range(200)
print "El número de fibonacci para 20 es",mimodulo.fib(20)
