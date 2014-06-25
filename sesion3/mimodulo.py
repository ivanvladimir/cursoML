#!/usr/bin/python
# -*- coding: utf-8 -*-

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


