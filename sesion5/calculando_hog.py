#!/usr/bin/python
# -*- coding: utf-8 -*-

# Se cargan módulos
import cv2
import argparse
import os.path

# Se configura los argumentos de la línea de comandos
p = argparse.ArgumentParser("mostrandoimagen.py")
p.add_argument("directorio",default=None,
            action="store", help="directorio de archivo a procesar")
opts = p.parse_args()

# Se lista el contenido de un directorio
listing=os.listdir(opts.directorio)

# Se filtra del directorio todo lo que no sea imagen (jpg o png)
listing=["{0}/{1}".format(opts.directorio,namefile) 
                        for namefile in listing if namefile.endswith('jpg') 
                                                or namefile.endswith('png')]

# Se configura al descriptor
hog = cv2.HOGDescriptor((48,48),(16,16),(8,8),(8,8),9)

# Por cada archivo en el directorio
for filename in listing:
    # Se abre la imagen
    img = cv2.imread(filename)

    # Se calcula el descriptor
    des=hog.compute(img)

    # Se imprime información del descriptor
    print "La imagen se redujo a",des.size
