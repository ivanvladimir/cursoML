#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2016/IIMAS/UNAM
# ----------------------------------------------------------------------

# Cargando librerias
from __future__ import division, print_function  # Python 2 users only
import argparse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report

if __name__ == "__main__":
    # Command line options
    p = argparse.ArgumentParser("Documentos")
    p.add_argument('TRAINIG',help="Archivos con datos de entreanmiento")
    p.add_argument('TESTING',help="Archivo con datos de prueba")
    p.add_argument("-v", "--verbose",
            action="store_true", dest="verbose",
            help="Modo verbose [Off]")
    p.add_argument('--version', action='version', version='create_segments 0.1')
    opts = p.parse_args()

    # Prepara función de verbose  -----------------------------------------
    if opts.verbose:
        def verbose(*args,**kargs):
            print(*args,**kargs)
    else:   
        verbose = lambda *a: None 

    X_train=[]
    Y_train=[]
    for line in open(opts.TRAINIG):
        line=line.strip()
        bits=line.rsplit(" ", 1)
        X_train.append(bits[0])
        Y_train.append(int(bits[1]))


    X_test=[]
    Y_test=[]
    for line in open(opts.TESTING):
        line=line.strip()
        bits=line.rsplit(" ", 1)
        X_test.append(bits[0])
        Y_test.append(int(bits[1]))

    count_vect = CountVectorizer()
    X_train    = count_vect.fit_transform(X_train)
    X_test     = count_vect.transform(X_test)

    clf = SVC()
    clf.fit(X_train, Y_train)

    Y_pred=clf.predict(X_test)
    print(clf.score(X_test,Y_test))
    print(classification_report(Y_test, Y_pred))
