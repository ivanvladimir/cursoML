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

listing=os.listdir(opts.directorio)
listing=["{0}/{1}".format(opts.directorio,namefile) 
                        for namefile in listing if namefile.endswith('jpg') 
                                                or namefile.endswith('png')]

hog = cv2.HOGDescriptor((48,48),(16,16),(8,8),(8,8),9)

for filename in listing:
    # Se abre la imagen
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    des=hog.compute(gray)

    print "Size of descriptor",des.size
