#!/usr/bin/python
# -*- coding: utf-8 -*-

# Se cargan módulos
import cv2
import argparse
import os.path
import numpy as np

# Se configura los argumentos de la línea de comandos
p = argparse.ArgumentParser("mostrandoimagen.py")
p.add_argument("positivos",default=None,
            action="store", help="directorio de archivo a procesar")
p.add_argument("negativos",default=None,
            action="store", help="directorio de archivo a procesar")
opts = p.parse_args()

listing=os.listdir(opts.positivos)
listing=["{0}/{1}".format(opts.positivos,namefile) 
                        for namefile in listing if namefile.endswith('jpg') 
                                                or namefile.endswith('png')]

hog = cv2.HOGDescriptor((48,48),(16,16),(8,8),(8,8),9)


trainData=[]
responses=[]
for filename in listing:
    # Se abre la imagen
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    des=hog.compute(gray)
    trainData.append(des)
    responses.append(1)

svm_params = dict( kernel_type = cv2.SVM_LINEAR,
                   svm_type = cv2.SVM_C_SVC,
                   C=2.67, gamma=5.383 )

svm = cv2.SVM()

trainData= np.float32(trainData).reshape(-1,900)
responses= np.float32(responses)
svm.train(trainData,responses,params=svm_params)

svm.save('model')

