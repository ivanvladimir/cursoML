import random

def tira(p):
    if random.uniform(0.0,1.0) <= p:
        return "s"
    else:
        return "a"


ejemplos_1=['s','s','s','a','s','s','a','a','s','s']
ejemplos_2=['s', 's', 'a', 'a', 's', 'a', 's', 's', 's', 'a', 's', 's', 's',
'a', 's', 's', 's', 'a', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's',
'a', 'a', 's', 's', 's', 's', 's', 's', 's', 's', 'a', 's', 's', 's', 's', 's',
's', 's', 's', 'a', 's', 's', 's', 's', 's', 's', 's', 'a', 's', 'a', 'a', 's',
's', 's', 's', 's', 's', 'a', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's',
's', 's', 's', 's', 's', 'a', 's', 's', 's', 's', 'a', 's', 'a', 'a', 's', 's',
's', 's', 's', 'a', 's', 'a', 's']

ejemplos=ejemplos_2

iters=100
model=0.5
models=[]
models_=[]
for i in range(iters):
    for e in ejemplos:
        actual=tira(model)
        if actual != e:
            if e=="s":
                model+=0.1
            else:
                model-=0.1
        models.append(model)
        models_.append(sum(models)/len(models))


print "Model",model
print "Len models", len(models)
print "Avg. model", models_[-1]
print "P(sol)", models_[-1]
print "P(aguila)",1-models_[-1]


import matplotlib.pyplot as plt

plt.clf()
x=range(len(models))
#plt.plot(x,models)
plt.plot(x,models_)
plt.show()
