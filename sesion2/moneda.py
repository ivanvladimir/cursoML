# -*- coding: utf-8 -*-
import random

def tira(p):
    if random.uniform(0.0,1.0) <= p:
        return "s"
    else:
        return "a"


data=['s','s','s','a','s','s','a','a','s','s']

iters=100
punishment=0.50
model=0.5
models=[]
models_=[]
for i in range(iters):
    for e in data:
        actual=tira(model)
        if actual != e:
            if e=="s":
                model+=punishment
            else:
                model-=punishment
        models.append(model)
        models_.append(sum(models)/len(models))



print "Iteraciones       :",iters
print "Total ejemplos    :",len(data)
print "Valor castigo     :",punishment
print "Último modelo     :",model
print "Modelos calculados:", len(models)
print "Modelo promedio   :", models_[-1]
print "P(sol)            :", models_[-1]
print "P(aguila)         :",1-models_[-1]

