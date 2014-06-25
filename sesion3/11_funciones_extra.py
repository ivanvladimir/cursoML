#!/usr/bin/python
# -*- coding: utf-8 -*-

# Parámetros opcionales
def count(palabra,ini=0,fin=20):
    for i in range(ini,fin):
        print palabra,i

    

print "Llamando con los parámetros explicitos, 'Contando...', 10 y 30"
count("Contando...",10,30)
print "Llamando sin el último parámetro"
count("Contando de nuevo...",15)
print "Llamando sin los dos parámetros opcionales"
count("Contando de nuevo otra vez...")
print "Llamando con los dos parámetros explicitos"
count("Contando de nuevo...",ini=3,fin=8)
print "Llamando con los dos parámetros explicitos pero no en orden"
count("Contando de nuevo...",fin=5,ini=3)

