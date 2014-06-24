#!/usr/bin/python

# Usando templates
lista=[(1,2),(2,3),(3,4),(4,5),(5,6)]
for val in lista:
    print "{1} {0}".format(val)

# Los templates se puedn usar para formatear 
lista=[(i*1.0/100,j*1.0/100) for i,j in lista]
for val in lista:
    print "{1:2.3f} {0:2.5f}".format(val)

# Convieriendo los elementos de la lista en cadenas
lista=["{1:2.3f}".format(i) for i,j in lista ]

# Creando una cadena de una lista de cadenas
print ":".join(lista)
