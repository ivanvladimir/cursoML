#!/usr/bin/python
# -*- coding: utf-8 -*-

# Se cargan módulos
import cv2
import argparse

# Se configura los argumentos de la línea de comandos
p = argparse.ArgumentParser("Extrae una region de una imagen")
p.add_argument("indice",default=None,type=int,
            action="store", help="Nombre de archivo")
opts = p.parse_args()

cap = cv2.VideoCapture(opts.indice)

while(True):
    # Lee un frame de la cámara
    ret, frame = cap.read()

    # Hace una transformación de la imagen
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Despliega el frame
    cv2.imshow('frame',gray)

    # Espera por una llave
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
