import random

random.seed()

tries=10
bias=.8
coins=[]

for i in range(tries):
    n=random.random()
    if n < bias:
        coins.append('s')
    else:
        coins.append('a')

print coins

