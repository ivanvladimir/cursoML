#!/usr/bin/python

# Importando un módulo 
import time
print "Hola..."
time.sleep(1)
print "...mundo!"

# Importando un funcion del modulo
from math import log
print "Log of 100",log(100)


# Cambiando el "namespace"
import random as ra
print "Escogeré un valor", ra.choice(['one','two','three'])




