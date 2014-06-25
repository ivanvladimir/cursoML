#!/usr/bin/python
# -*- coding: utf-8 -*-

# Importando un módulo 
import time
print "Hola..."
time.sleep(1)
print "...mundo!"

# Checando el contenido de la función
print "Esta es la ayuda del modulo time... preciona 'q' para salir"
help(time)

# Importando un funcion del modulo
from math import log
print "Log of 100",log(100)


# Cambiando el "namespace"
import random as ra
print "Escogeré un valor", ra.choice(['one','two','three'])




