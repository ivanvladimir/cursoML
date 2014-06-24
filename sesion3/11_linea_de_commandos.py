#!/usr/bin/python

import argparse

p = argparse.ArgumentParser("Author identification")
p.add_argument("Archivo_1",default=None,
            action="store", help="Archivo Uno")
p.add_argument("Archivo_2",default=None,
            action="store", help="Archivo Dos")
p.add_argument("-o", "--opcion1",default=None,type=str,
            action="store", dest="op_1",
            help="Opcion 2")
p.add_argument("", "--opcion2",default="Valor2",type=str,
            action="store", dest="op_2",
            help="Opcion 2")
p.add_argument("-n", "--nueva_opcion",default="Valor3",type=str,
            action="store", dest="op_3",
            help="Argumento")

opts = p.parse_args()

print "Primer argumento",opts.Archivo_1
print "Segundo argumento",opts.Archivo_2
print "Primera opción",opts.op_1
print "Segundo opción",opts.op_3
print "Tercera opcóón",opts.op_3

