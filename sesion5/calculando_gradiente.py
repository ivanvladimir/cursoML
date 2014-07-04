#!/usr/bin/python
# -*- coding: utf-8 -*-

# Se cargan módulos
import cv2
import argparse
import os.path

# Se configura los argumentos de la línea de comandos
p = argparse.ArgumentParser("mostrandoimagen.py")
p.add_argument("archivo",default=None,
            action="store", help="directorio de archivo a procesar")
opts = p.parse_args()


# Se abre la imagen
img = cv2.imread(opts.archivo)

# Hace una transformación de la imagen
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# Se calcula el descriptor
des=cv2.Laplacian(gray,cv2.CV_64F)

# Se desplieage imagen
cv2.imshow("Gradiente "+opts.archivo,des)

# Se espera por que se oprima una tecla
print "Oprima una tecla para continuar"
cv2.waitKey(0)

sobelx = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=5)
# Se desplieage imagen
cv2.imshow("Gradiente en x "+opts.archivo,sobelx)

# Se espera por que se oprima una tecla
print "Oprima una tecla para continuar"
cv2.waitKey(0)


sobely = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=5)
# Se desplieage imagen
cv2.imshow("Gradiente en x "+opts.archivo,sobely)

# Se espera por que se oprima una tecla
print "Oprima una tecla para continuar"
cv2.waitKey(0)


