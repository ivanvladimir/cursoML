#!/usr/bin/python
# -*- coding: utf-8 -*-

# Se cargan módulos
import cv2
import argparse

# Se configura los argumentos de la línea de comandos
p = argparse.ArgumentParser("mostrandoimagen.py")
p.add_argument("archivo",default=None,
            action="store", help="Nombre de archivo")
opts = p.parse_args()

# Se abra la imagen
img = cv2.imread(opts.archivo)

# Se espera por que se oprima una tecla
print "Oprima una tecla para cerrar"
cv2.waitKey(0)
