#!/usr/bin/python

# Esta función no regresa ningún valor, pero hace algo
def print_percentage(val):
    per=val*100
    print str(per)+"%"

# Esta funcion suma los valores de una lista y regresa el resultado
def suma_lista(lista):
    val=0
    for l in lista:
        val+=1
    return val

# Esta función es recursiva
def fib(n):
    if n < 2:
        return n
    return fib(n-2) + fib(n-1)


print "El porcentage de 0.1 es"
print_percentage(0.1)

print "El porcentage de 0.02 es"
print_percentage(0.02)

lista=range(20)
print "La suma de la lista",lista,"es",suma_lista(lista)
lista=range(200)
print "La suma de la lista",lista,"es",suma_lista(lista)

lista=range(20)
print "El número de fibonacci para 10 es",fib(10)
lista=range(200)
print "El número de fibonacci para 20 es",fib(20)


