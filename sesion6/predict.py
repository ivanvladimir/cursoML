#!/usr/bin/python
# -*- coding: utf-8 -*-

# Se cargan módulos
import cv2
import argparse
import os.path
import numpy as np
import random

# Se configura los argumentos de la línea de comandos
p = argparse.ArgumentParser("mostrandoimagen.py")
p.add_argument("test",default=None,
            action="store", help="directorio con figuras recordadas")
p.add_argument("-m","--model",default="model.svm",
            action="store", help="Modelo de SVM")
opts = p.parse_args()

listing=os.listdir(opts.test)
listing=["{0}/{1}".format(opts.test,namefile) 
                        for namefile in listing if namefile.endswith('jpg') 
                                                or namefile.endswith('png')]

hog = cv2.HOGDescriptor((48,48),(16,16),(8,8),(8,8),9)


svm = cv2.SVM()
svm.load(opts.model)

print "Testing"
total=0
res=0
for filename in listing:
    # Se abre la imagen
    img = cv2.imread(filename)


    des=hog.compute(img)
    res+=svm.predict(des)
    total+=1

print "Right",res
print "Total", total

