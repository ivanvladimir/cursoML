#!/usr/bin/python
# -*- coding: utf-8 -*-

lista=range(100)
residuos_3={}

for i in lista:
    try:
        residuos_3[i%3]+=1
    except KeyError:
        residuos_3[i%3]=0

print residuos_3
