#!/usr/bin/python
# -*- coding: utf-8 -*-

# Se cargan módulos
import cv2
import argparse

# Se configura los argumentos de la línea de comandos
p = argparse.ArgumentParser("Extrae una region de una imagen")
p.add_argument("x1",default=None,type=int,
            action="store", help="Cordenada x de primera esquina")
p.add_argument("y1",default=None,type=int,
            action="store", help="Cordenada y de primera esquina")
p.add_argument("x2",default=None,type=int,
            action="store", help="Cordenada x de segunda esquina")
p.add_argument("y2",default=None,type=int,
            action="store", help="Cordenada y de segunda esquina")
p.add_argument("archivo",default=None,
            action="store", help="Nombre de archivo")
opts = p.parse_args()


# Se checa que las cordenadas sean válidas
if opts.x1>=opts.x2:
    p.error("Error coordenadas x1 ({0}) y x2 ({1}) incorrectas".format(opts.x1,opts.x2))

if opts.y1>=opts.y2:
    p.error("Error coordenadas x1 ({0}) y x2 ({1}) incorrectas".format(opts.x1,opts.x2))

# Se lee la imagen
img = cv2.imread(opts.archivo)

# Se extraé las propiedades de la imagen
height, width, depth = img.shape

# Se checa que las cordenadas sean válidas para la imagen
if opts.x1>width or opts.x2>width:
    p.error("Cordenadas más grande que el ancho de la imagen ({0})".format(width))
    p.error()

if opts.y1>height or opts.y2>height:
    p.error("Cordenadas más grande que el ancho de la imagen ({0})".format(width))

# Se corta la región de interes
crop_img = img[opts.y1:opts.y2, opts.x1:opts.x2]

# Se guarda la imagen
cv2.imwrite("imagen_recortada.png", crop_img)

