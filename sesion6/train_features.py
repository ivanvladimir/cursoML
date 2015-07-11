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
p.add_argument("positivos",default=None,
            action="store", help="directorio de archivo a procesar")
p.add_argument("negativos",default=None,
            action="store", help="directorio de archivo a procesar")
p.add_argument("-m","--model",default="model.svm",
            action="store", help="Modelo de SVM")
opts = p.parse_args()

listing=os.listdir(opts.positivos)
listing=["{0}/{1}".format(opts.positivos,namefile) 
                        for namefile in listing if namefile.endswith('jpg') 
                                                or namefile.endswith('png')]

hog = cv2.HOGDescriptor((48,48),(16,16),(8,8),(8,8),9)


trainData=[]
print "Generating samples"
for filename in listing:
    # Se abre la imagen
    img = cv2.imread(filename)
    #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    des=hog.compute(img)
    trainData.append((des,1))


listing=os.listdir(opts.negativos)
listing=["{0}/{1}".format(opts.negativos,namefile) 
                        for namefile in listing if namefile.endswith('jpg') 
                                                or namefile.endswith('png')]

print len(trainData)
print "Generating samples"
for filename in listing:
    # Se abre la imagen
    img = cv2.imread(filename)
    #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    height, width, depth = img.shape

    for i in range(10):
        h=random.randint(0,height-48)
        w=random.randint(0,width-48)

        sample_img=img[h:h+48,w:w+48]

        des=hog.compute(sample_img)
        trainData.append((des,0))

random.shuffle(trainData)
trainData,responses=zip(*trainData)


print len(responses)
print "Training"
svm_params = dict( kernel_type = cv2.SVM_LINEAR,
                   svm_type = cv2.SVM_NU_SVC,
                   C=2.67, gamma=5.383, nu=0.1 )

svm = cv2.SVM()

trainData= np.float32(trainData).reshape(-1,900)
responses= np.float32(responses)
svm.train_auto(trainData,responses,None,None,params=svm_params,k_fold=10)

svm.save(opts.model)

