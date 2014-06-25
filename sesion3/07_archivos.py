#!/usr/bin/python

#Generando un archivo
archivo=open('tmp','w')
for i in range(10):
    print >> archivo, i, "hola mundo!"
archivo.close()

#Abriendo archivio
archivo=open('tmp',"r")
for linea in archivo:
    print linea
archivo.close()

#Arreglando problema con linea
archivo=open('tmp')
for linea in archivo:
    line=linea.strip()
    print linea
archivo.close()

#Imprimiento la última palabra
archivo=open('tmp')
for linea in archivo:
    line=linea.strip()
    bits=line.split()
    print bits[-1]
archivo.close()

