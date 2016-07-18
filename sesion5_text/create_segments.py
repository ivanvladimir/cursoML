#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2016/IIMAS/UNAM
# ----------------------------------------------------------------------

# Cargando librerias
from __future__ import division, print_function  # Python 2 users only
import argparse
import nltk, re, pprint
from nltk import word_tokenize


if __name__ == "__main__":
    # Command line options
    p = argparse.ArgumentParser("Documentos")
    p.add_argument('LISTA',help="Archivo con lista",nargs='+')
    p.add_argument("-t", "--train",default=0.7,
            action="store", dest="train",
            help="Percentage of document for training [0.7]")
    p.add_argument("-s", "--size",default=500,type=int,
            action="store", dest="size",
            help="Number of tokens in segment [500]")
    p.add_argument("-j", "--jump",default=250,type=int,
            action="store", dest="jump",
            help="Skip size betweent tokens [250]")
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


    segs_train=[]
    segs_test=[]
    for i,filename in enumerate(opts.LISTA):
        raw = open(filename).read().decode('utf8')
        tokens = word_tokenize(raw)
        # training segment
        train = tokens[0:int(0.7*len(tokens))]
        for j in range(0,len(train),opts.jump):
            seg=train[j:j+opts.size]
            segs_train.append((" ".join(seg).encode('utf8'),i))
        # testing segment
        test = tokens[int(0.7*len(tokens)):]
        for j in range(0,len(test),opts.jump):
            seg=test[j:j+opts.size]
            segs_test.append((" ".join(seg).encode('utf8'),i))


    examples=open("train.txt",'w')
    for seg in segs_train:
        print(seg[0],seg[1],file=examples)
    examples.close()
    examples=open("test.txt",'w')
    for seg in segs_test:
        print(seg[0],seg[1],file=examples)
    examples.close()

