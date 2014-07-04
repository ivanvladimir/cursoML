#!/usr/bin/python
# -*- coding: utf-8 -*-

# Se cargan módulos
import cv2
import argparse

# Se configura los argumentos de la línea de comandos
p = argparse.ArgumentParser("mostrandoimagen.py")
p.add_argument("archivo",default=None,
            action="store", help="Nombre de archivo")
p.add_argument("-x",default=100,type=int,
            action="store", help="No. pixeles en x")
p.add_argument("-y",default=100,type=int,
            action="store", help="No. pixels en y")

opts = p.parse_args()

# Se abra la imagen
img = cv2.imread(opts.archivo)

# Se cambia el tamaño de la imagen
nimg = cv2.resize(img, (opts.x, opts.y))

# Se desplieage imagen
cv2.imshow("Mostrando imagen: "+opts.archivo,nimg)

# Se espera por que se oprima una tecla
print "Oprima una tecla para cerrar"
cv2.waitKey(0)
