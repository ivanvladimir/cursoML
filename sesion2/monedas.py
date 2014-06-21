import random

def tira(p):
    if random.random() >= p:
        return "s"
    else:
        return "a"


monedas=[0.9,0.9,0.9,0.9,0.5,0.9]

m=2000

data=[]
for moneda in monedas:
    data.append([])
    for i in range(m):
        data[-1].append(tira(moneda))


iters=200
model=[0.5 for x in monedas]
models=[[] for x in monedas]
models_=[[] for x in monedas]
for i in range(iters):
    for moneda,ejemplos in enumerate(data):
        for e in ejemplos:
            actual=tira(model[moneda])
            if actual != e:
                if e=="s":
                    model[moneda]-=0.1
                else:
                    model[moneda]+=0.1
            models[moneda].append(model[moneda])
        models_[moneda].append(sum(models[moneda])/len(models[moneda]))


print "Model",model
print "Len models", len(models)
print "Avg. model", [x[-1] for x in models_]

import matplotlib.pyplot as plt

plt.clf()
#plt.plot(x,models)
for data in models_:
    x=range(len(data))
    plt.plot(x,data)
plt.show()
