#!/usr/bin/python
# -*- coding: utf-8 -*-

# Usando templates
lista=[(1,2),(2,3),(3,4),(4,5),(5,6)]
for val0,val1 in lista:
    print "{1} {0}".format(val0,val1)

# Los templates se puedn usar para formatear 
lista=[(i*1.0/100,j*1.0/100) for i,j in lista]
for val0,val1 in lista:
    print "{1:2.3f} {0:2.5f}".format(val0,val1)

# Convieriendo los elementos de la lista en cadenas
lista=["{0:2.3f}".format(i) for i,j in lista ]

# Creando una cadena de una lista de cadenas
print ":".join(lista)
